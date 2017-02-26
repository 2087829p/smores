import json
import requests

__author__ = 'tony petrov'

import datetime

import twython
from twython import TwythonStreamer, TwythonError
import random
import string
import constants
from utils import user_filter
import storage as st
import test_struct as test
import pytumblr
import threading
import facebook
import time
import copy


class TwitterStreamer(TwythonStreamer):
    def set_callback(self, callback):
        self._callback = callback

    def set_error_handler(self, handler):
        self._error_handler = handler

    def on_success(self, data):
        if data:
            self._callback(data)

    def on_error(self, status_code, data):
        print status_code
        self._error_handler()


class Credentials_Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Rate_Limit_Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TwitterHandler:
    def __init__(self, acc_details, read_only=False, **kwargs):
        self.id = kwargs['id']
        if not acc_details or not 'app_key' in acc_details:
            raise Credentials_Error('Missing account credentials')
        if constants.TESTING:
            self._twitter = test.MockTwitter()
        else:
            try:
                if read_only:
                    self._twitter = twython.Twython(acc_details['app_key'], acc_details['app_secret'], oauth_version=2)
                    acc_details['oauth_token'] = self._twitter.obtain_access_token()
                else:
                    if 'client_args' in kwargs:
                        self._twitter = twython.Twython(acc_details['app_key'], acc_details['app_secret'],
                                                        acc_details['oauth_token'], acc_details['oauth_token_secret'],
                                                        client_args=kwargs['client_args'])
                    else:
                        self._twitter = twython.Twython(acc_details['app_key'], acc_details['app_secret'],
                                                        acc_details['oauth_token'], acc_details['oauth_token_secret'])

                self.acc_details = acc_details
            # self._auth=self._handlers.get_authentication_tokens()
            # self._lists=self._handlers.show_owned_lists()#get lists that the user has
            except Exception as e:
                print "Unable to login to twitter cause " + e.message
                import sys
                sys.exit()
        self._scheduler = kwargs.get('scheduler', None)
        self._list_attempts = 15
        self._wait_for = [0 for i in range(4)]

    def can_fetch(self):
        if (len(self._wait_for) == 0):
            return True
        # checks if any operation has been time limited and if so checks if the time limit has passed
        return any(d + datetime.timedelta(minutes=15) < datetime.datetime.now() for d in self._wait_for)

    # Tries to fit new twitter accounts into either the twitter lists or the bulk lists
    def fit_to_lists(self, candidates, lists, max_list_num, max_list_size, is_twitter_list):
        """ Tries to fit the given candidate users in to either a twitter list or in to a bulk list  """
        # check if lists are maxed out
        if (len(lists) > max_list_num) and lists[-1]['count'] >= max_list_size:
            return candidates
        if len(candidates) == 0:
            return []
        # check if we have any lists and if the last list has enough space to fit any of the candidates
        if len(lists) > 0 and lists[-1]['count'] < max_list_size:
            # determine the max amount of users the list can take have no more than the remaining capacity of the list
            take = min(max_list_size - lists[-1]['count'], len(candidates))
            # determine whether the candidates should go to the twitter lists or bulk lists
            if is_twitter_list:
                if self._list_attempts <= 0:
                    lists[-1]['count'] = self._twitter.get_specific_list(list_id=lists[-1]['id'])['member_count']
                    return candidates
                try:
                    take = min(constants.TWITTER_ADD_TO_LIST_LIMIT, take)
                    # use the api to add the new users to the list
                    self._list_attempts -= 1
                    self._twitter.create_list_members(list_id=lists[-1]['id'],
                                                      user_id=','.join(map(lambda x: str(x), candidates[:take])))
                    # update the size of the list
                    lists[-1]['count'] = lists[-1]['count'] + take
                except Exception as e:
                    print "Users could not be added to list in bulk cause: %s" % e.message
                    # twitter's bulk adding is bugged
                    print "Trying to add users 1 by 1"
                    try:
                        self._twitter.add_list_member(list_id=lists[-1]['id'], user_id=candidates[0])
                        lists[-1]['count'] = lists[-1]['count'] + 1
                    except Exception as e:
                        print "Adding users to list failed cause: %s" % e.message
                        self._list_attempts = 0
                    # error occurred can not put anything into the list return the remaining number of candidates
                    return candidates
            else:
                # put users into the last bulk list
                lists[-1]['ids'] += candidates[:take]
                # update the bulk list's size
                lists[-1]['count'] = len(lists[-1]['ids'])
            # remove the users we just added
            candidates = candidates[take:]
            # recurse and attempt to fit in more users
            return self.fit_to_lists(candidates, lists, max_list_num, max_list_size, is_twitter_list)
        # either no free list was found or no lists exist
        else:
            if is_twitter_list:
                try:
                    # create a new twitter list
                    list_id = \
                    self._twitter.create_list(name=''.join(random.choice(string.lowercase) for i in range(12)),
                                              mode='public')['id']
                    # add it to the crawler data base
                    lists.append({'id': list_id, 'count': 0})
                    if self._scheduler:
                        self._scheduler.__put_data__(constants.TASK_FETCH_LISTS, {'id': list_id, 'count': 0})
                        # recurse and try to fill the new list
                    return self.fit_to_lists(candidates, lists, max_list_num, max_list_size, is_twitter_list)
                except Exception as e:
                    print "Twitter List could not be created " + e.message
            else:
                # calculate how many users we can take into a bulk list
                take = min(max_list_size, len(candidates))
                new_list = {'ids': candidates[:take], 'count': take}
                # create a new bulk list for our users and put them in it
                lists.append(new_list)
                if self._scheduler:
                    self._scheduler.__put_data__(constants.TASK_BULK_RETRIEVE, new_list)
                    # remove the users we just added
                candidates = candidates[take:]
                # recurse and attempt to fit them into the same or new list
                return self.fit_to_lists(candidates, lists, max_list_num, max_list_size, is_twitter_list)
        # return the remaining users which we could not add to any list
        return candidates

    def __follow_users__(self, candidates, users, following):
        try:
            if candidates and following < constants.MAX_FOLLOWABLE_USERS:
                # follow all the remaining users which we couldn't find a place for
                import time
                import random
                take = min(constants.TWITTER_MAX_FOLLOW_REQUESTS, len(candidates))
                for i in xrange(take):
                    try:
                        self._twitter.create_friendship(user_id=candidates[i], follow=True)
                        time.sleep(random.randint(1,
                                                  15))  # sleep for random amount of seconds to avoid twitter thinking that we're automated
                    except:
                        print "Could not follow user " + str(candidates[i])
                        return candidates
                candidates = candidates[take:]
            if candidates:
                # if there are some users remaining see if we have space to follow their timeline without following them
                take = min(constants.TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS, len(candidates))
                members = candidates[:take]
                users += members
                if self._scheduler:
                    self._scheduler.__put_data__(constants.TASK_FETCH_USER, members)
                candidates = candidates[take:]
        except Exception as e:
            print e.message
        return candidates

    def __get_friends_and_followers__(self, id, rqs_remaining):
        """ Fetches the friends or followers of a specific user """
        users = []
        try:
            # check if we have any get id requests remaining if so get the data and decrement
            if (rqs_remaining[0] > 0):
                users += self._twitter.get_friends_ids(user_id=id)["ids"]
                users += self._twitter.get_followers_ids(user_id=id)["ids"]
                rqs_remaining[0] -= 1
            # check if we have any get list of user requests remaining
            elif (rqs_remaining[1] > 0):
                users += [x["id"] for x in user_filter(self._twitter.get_friends_list(user_id=id)["users"])]
                users += [x["id"] for x in user_filter(self._twitter.get_followers_list(user_id=id)["users"])]
                rqs_remaining[1] -= 1
        except TwythonError as e:
            if e.error_code == 404:
                print "User " + str(id) + "could not be found"
            else:
                print e.message
        except Exception as e1:
            print "An error occurred while getting friends and followers " + e1.message
            rqs_remaining[0] = 0
            rqs_remaining[1] = 0
        return users

    # attempts to find new accounts to follow
    def explore(self, args):
        """Find new users to follow"""
        remaining = args.get('remaining', [])
        candidates = []
        self._list_attempts = 15
        user_lists = args.get('user_lists', [])
        bulk_lists = args.get('bulk_lists', [])
        users = args.get('total_followed', [])
        total_followed = copy.deepcopy(users)
        try:
            # get our suggested categories
            print "collecting slugs"
            slugs = self._twitter.get_user_suggestions()
            data = self._twitter.verify_credentials()
            # get the people who we are following
            following = self._twitter.get_friends_ids(screen_name=data['screen_name'])
            print "%d users followed online" % len(following['ids'])
            total_followed += following['ids'] + ([i for sl in bulk_lists for i in sl['ids']] if bulk_lists else [])
            print "%d total users followed offline" % (len(total_followed) - len(following['ids']))
            # get the total number of twitter users that we follow including bulk list users and twitter list users as well as non followed users
            ff_requests = [14, 15]  # friends_ids and followers_ids requests remaining
            for s in [random.choice(slugs) for i in xrange(15)]:
                # get some suggested users in the given category
                new_users = list()
                try:
                    new_users = self._twitter.get_user_suggestions_by_slug(slug=s['slug'])['users']
                except TwythonError as e:
                    if e.error_code == 404:
                        print "Slug " + s['name'] + " could not be found"
                    else:
                        print "Could not retrieve data for slug = " + str(s['name']) + " due to " + e.message
                    continue
                new_users = sorted(new_users, key=lambda k: k['friends_count'])
                new_users.reverse()
                new_users = [u['id'] for u in user_filter(new_users)]
                friends = []
                if ff_requests[0] > 0 or ff_requests[1] > 0:
                    for u in new_users:
                        friends += self.__get_friends_and_followers__(u, ff_requests)
                # get the users which we currently do not follow only
                candidates += list(set(new_users + friends) - set(total_followed + remaining))
            # try to fit some of the candidates into the twitter lists
            print str(len(candidates)) + " new users found"
            candidates = candidates + remaining
            candidates_total = len(candidates)
            candidates = self.fit_to_lists(candidates, user_lists,
                                           constants.TWITTER_MAX_NUMBER_OF_LISTS * constants.TWITTER_CYCLES_PER_HOUR,
                                           constants.TWITTER_MAX_LIST_SIZE, True)
            print str(candidates_total - len(candidates)) + " users added to twitter lists"
            candidates_total = len(candidates)
            # try to fit some users into the bulk lists
            candidates = self.fit_to_lists(candidates, bulk_lists,
                                           constants.TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE * constants.TWITTER_CYCLES_PER_HOUR,
                                           constants.TWITTER_BULK_LIST_SIZE, False)
            print str(candidates_total - len(candidates)) + " users added to bulk lists"
            candidates_total = len(candidates)
            self.__follow_users__(candidates, users, len(following))
            print "%d users added to offline following" % (candidates_total - len(candidates))
            print str(len(candidates)) + " users left unallocated"
        except Exception as e:
            print "Error while exploring " + e.message
            if candidates:
                candidates = self.fit_to_lists(candidates, user_lists,
                                               constants.TWITTER_MAX_NUMBER_OF_LISTS * constants.TWITTER_CYCLES_PER_HOUR,
                                               constants.TWITTER_MAX_LIST_SIZE, True)
                candidates = self.fit_to_lists(candidates, bulk_lists,
                                               constants.TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE * constants.TWITTER_CYCLES_PER_HOUR,
                                               constants.TWITTER_BULK_LIST_SIZE, False)
                self.__follow_users__(candidates, users, constants.MAX_FOLLOWABLE_USERS)
        if constants.TESTING:
            return []
        st.save_data(user_lists, constants.TWITTER_LIST_STORAGE)
        st.save_data(bulk_lists, constants.TWITTER_BULK_LIST_STORAGE)
        st.save_data(users, constants.TWITTER_USER_STORAGE)
        return candidates

    # fetches the crawler's timeline id specifies the id of the last returned tweet, if since is true
    # crawler returns tweets that were posted after the given id
    def fetch_home_timeline(self, task_data):
        data = []
        max_attempts = 15  # 15 is the max number of requests we can send for our timeline
        current_id = task_data["id"]
        update_fq = 60
        while max_attempts > 0:
            temp_data = []
            if current_id == 0:
                # if first run
                # get timeline
                temp_data += self._twitter.get_home_timeline()
                # set current_id to the last id since we will request the old timeline
                current_id = temp_data[-1]["id"]
                # set task id to the top id since next time we will request the up to date timeline
                task_data["id"] = temp_data[0]["id"]
            elif task_data.get('since', False):
                # requesting only new tweets
                # sleep for 1 min to allow the timeline to refresh
                time.sleep(update_fq)
                # get data
                temp_data += self._twitter.get_home_timeline(since_id=current_id)
                # update current id and task id
                current_id = temp_data[0]["id"]
                task_data["id"] = current_id
            else:
                # collecting data for old tweets
                temp_data += self._twitter.get_home_timeline(max_id=current_id)
                current_id = temp_data[-1]["id"]
            data += temp_data
            max_attempts -= 1
        # tell worker that next time we want the new tweets only
        task_data['since'] = True
        st.save_data(task_data, constants.TWITTER_WALL_STORAGE)
        return data

    # fetches the specified user's timeline
    def fetch_user_timeline(self, user):
        # count is set to 200 since that's the max that twitter would actually return despite the docs saying 3200
        return self._twitter.get_user_timeline(user_id=user, count=200)  # user = 900 , app = 1500

    # fetches the tweets in the specified list of _users
    def fetch_list_tweets(self, list):
        return self._twitter.get_list_statuses(list_id=list['id'])  # 900

    # fetches the latest tweets of up to 100 _users
    # as specified in the user_ids list
    def fetch_bulk_tweets(self, user_ids):
        data = self._twitter.lookup_user(user_id=','.join(map(lambda x: str(x), user_ids['ids'])),
                                         include_entities=True)  # user = 900, app = 300
        # convert data from user info to tweet
        ret_data = []
        for i in data:
            if 'status' in i:
                tweet = i['status']
                i.pop('status')
                tweet['user'] = i
                ret_data.append(tweet)
        return ret_data

    def search(self, q_params):
        max_attempts = 180
        query_max_length = 500
        data = []
        keywords = q_params['keywords']
        keywords.reverse()
        while max_attempts > 0 and len(keywords) > 0:
            query = keywords.pop()
            if len(keywords) > 1:
                current_length = len(query)
                while current_length < query_max_length:
                    op = ' OR '
                    if current_length + len(op) + len(keywords[-1]) < query_max_length:
                        query += op + keywords.pop()
                        current_length = len(query)
                    else:
                        break
            # keywords = ' OR '.join(keywords)
            max_attempts -= 1
        try:
            data += self._twitter.search(q=query, count=100, include_entities=True).get('statuses', [])
        except Exception as e:
            print query
            print "Search failed cause: %s" % e.message
        return data

    def get_trends(self, args):
        trends = []
        trend_filter = lambda data: map(lambda x: x['name'], data)
        max_attempts = args.get('attempts', constants.MAX_TWITTER_TRENDS_REQUESTS)
        if max_attempts == 0:
            return []
        if 'woeid' in args:
            # search_queries for trends at a location with a specific where on earth id
            try:
                # go through left over woeids
                for w in args['woeid'][:max_attempts]:
                    tmp = self._twitter.get_place_trends(id=w)
                    for t in tmp:
                        # filter each group of trends
                        trends += trend_filter(t['trends'])
                    max_attempts -= 1
            except:
                return trends
        elif 'lat' in args and 'long' in args:
            # search_queries for trends in a given geo box based on lat and long
            try:
                tmp = self._twitter.get_closest_trends(lat=args['lat'], long=args['long'])
                for t in tmp:
                    trends += trend_filter(t['trends'])
            except:
                return trends
        else:
            # no location specified or the location is specified by name
            # get relevant locations
            locations = self._twitter.get_available_trends()
            if 'location' in args:
                # if any locations were specified by name filter the woeids based on region
                loc = args['location'].lower()
                locations = filter(lambda x: x['country'].lower() == loc or
                                             x['name'].lower() == loc or
                                             x['countryCode'].lower() == loc,
                                   locations)
            # get woeids
            locations = map(lambda x: x['woeid'], locations)
            # get trends
            trends += self.get_trends(dict(woeid=locations, attempts=max_attempts))
        return trends


class TumblrHandler:
    def __init__(self, credentials):
        self._client = pytumblr.TumblrRestClient(
            credentials['oauth_key'], credentials['oauth_secret'], credentials['token'], credentials['token_secret']
        )
        self._rqs_per_cycle_remaining = constants.TUMBLR_MAX_REQUESTS_PER_HOUR
        self._rqs_for_the_day = constants.TUMBLR_MAX_REQUESTS_PER_DAY
        self._lock = threading.Lock()

    def __dec_remaining_rqs__(self):
        with self._lock:
            self._rqs_per_cycle_remaining -= 1
            self._rqs_for_the_day -= 1

    def reset_requests(self):
        if self._rqs_for_the_day > 0:
            self._rqs_per_cycle_remaining = constants.TUMBLR_MAX_REQUESTS_PER_HOUR

    def reset_daily_requests(self):
        with self._lock:
            self._rqs_for_the_day = constants.TUMBLR_MAX_REQUESTS_PER_DAY

    def __get_rqs_remaining__(self):
        ret = 0
        with self._lock:
            ret = self._rqs_per_cycle_remaining
        return ret

    def get_dashboard(self, last_id):
        if self.__get_rqs_remaining__() <= 0:
            return []
        data = self._client.dashboard()
        while (data[-1]['id'] != last_id) or self.__get_rqs_remaining__() > 0:
            data += self._client.dashboard()
            self.__dec_remaining_rqs__()
        return self._client.dashboard()

    def follow(self, user_id):
        self.__dec_remaining_rqs__()
        self._client.follow(user_id)

    def get_post_with_tag(self, tag_info):
        if self.__get_rqs_remaining__() <= 0:
            return []
        self.__dec_remaining_rqs__()
        return self._client.tagged(tag_info['tags'], filter=tag_info['filter'])

    def get_blog_posts(self, blog):
        if self.__get_rqs_remaining__() <= 0:
            return []
        self.__dec_remaining_rqs__()
        return self._client.posts(blog)


class FacebookHandler:
    def __init__(self, token):
        self._graph = facebook.GraphAPI(access_token=token, version='2.1')
        self._rqs_per_cycle_remaining = constants.FACEBOOK_MAX_REQUESTS_PER_HOUR
        self._rqs_for_the_day = constants.FACEBOOK_MAX_REQUESTS_PER_HOUR * 24
        self._lock = threading.Lock()

    def __dec_remaining_rqs__(self):
        with self._lock:
            self._rqs_per_cycle_remaining -= 1
            self._rqs_for_the_day -= 1

    def __dec_remaining_rqs_by__(self, amount):
        with self._lock:
            self._rqs_per_cycle_remaining -= amount
            self._rqs_for_the_day -= amount

    def __get_rqs_remaining__(self):
        ret = 0
        with self._lock:
            ret = self._rqs_per_cycle_remaining
        return ret

    def reset_requests(self):
        if self._rqs_for_the_day > 0:
            self._rqs_per_cycle_remaining = constants.FACEBOOK_MAX_REQUESTS_PER_HOUR

    def reset_daily_requests(self):
        with self._lock:
            self._rqs_for_the_day = constants.FACEBOOK_MAX_REQUESTS_PER_HOUR * 24

    def get_posts_for_users(self, user_ids):
        if len(user_ids) > self.__get_rqs_remaining__():
            raise Rate_Limit_Error('Request will exceed Facebook rate limit')
        # must decrease by number of all ids we requested cause facebook counts every id as a request
        self.__dec_remaining_rqs_by__(len(user_ids))
        url = 'https://graph.facebook.com/posts?ids=%s' % ','.join(user_ids)
        parameters = {'access_token': self._graph.access_token}
        r = requests.get(url, params=parameters)
        result = json.loads(r.text)
        return result

    def get_my_wall(self, **kwargs):
        if self.__get_rqs_remaining__() <= 0:
            raise Rate_Limit_Error('Facebook rate limit reached')
        self.__dec_remaining_rqs__()
        return self._graph.get_object('me/posts')['data']
