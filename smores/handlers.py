__author__ = 'tony petrov'

import datetime

import twython
from twython import TwythonStreamer

from smores import constants


class Handler:
    def fetch_data(self):
        return
    def expolore(self):
        return
    def can_fetch(self):
        return True

#stream = MyStreamer(APP_KEY, APP_SECRET,
#                   OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
#stream.statuses.filter(track='twitter')
class TwitterStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            print data['text'].encode('utf-8')

    def on_error(self, status_code, data):
        print status_code
        self.disconnect()


class TwitterHandler(Handler):

    def __init__(self,acc_details,workdata):
        try:
            self._twitter=twython.Twython(acc_details['app_key'], acc_details['app_secret'],acc_details['oauth_token'],acc_details['oauth_token_secret'])
            self._auth=self._twitter.get_authentication_tokens()
            self._lists=self._twitter.show_owned_lists()#get lists that the user has
        except:
            print "Unable to login to twitter"
            return
        #users-dict[id(specifies the tweeter id of the user),current_tweet(specifies the id of the last tweet fetched by the crawler)]
        self._users=workdata['_users'] if '_users' in workdata.keys() else []#get the _users that we don't follow but want tweets from
        #user_lists-dict[id,count]
        self._user_lists=workdata['user_lists'] if 'user_lists' in workdata.keys() else []#get twitter lists containing up to 5000 users each
        #_bulk_lists-dict[id,count]
        self._bulk_lists=workdata['bulk_lists'] if 'bulk_lists' in workdata.keys else []#get list of dict containing 100 twitter users each used in the fetch_bulk_tweets function
        self._wait_for=[0 for i in range(4)]

    def fetch_data(self):
        data=self.fetch_home_timeline({"id":0,"since":False})
        for u in self._users:
            data+=self.fetch_user_timeline(u['id'])
        for l in self._lists:
            data+=self.fetch_list_tweets(l)
        for ul in self._user_lists:
            data+=self.fetch_bulk_tweets(ul['id'])
        return data
    #checks to see if fetching data at this time is possible based on the twitter timeout
    def can_fetch(self):
        if(len(self._wait_for)==0):
            return True
        #checks if any operation has been time limited and if so checks if the time limit has passed
        return any(d+datetime.timedelta(minutes=15)<datetime.datetime.now() for d in self._wait_for)

    #get the ids of all members of lists that the crawler has
    def get_list_members(self,lists):
        list_members=[]
        try:
            if lists:
                #lists=self._twitter.show_lists()
                #self._user_lists=[ul['list_id'] for ul in self._user_lists]
                for l in self._user_lists:
                    list_members+=self._twitter.get_list_members(list_id=l)
        except:
            print "An Error Occurred"
        return list_members

    #Tries to fit new twitter accounts into either the twitter lists or the bulk lists
    def fit_to_lists(self,candidates,lists,max_list_num,max_list_size,is_twitter_list):
        #check if lists are maxed out
        if(len(lists)>max_list_num) and lists[-1]['count']>=max_list_size:
            return candidates
        if(len(candidates)==0):
            return []
        #check if we have any lists
        if len(lists)>0:
            #check if the last list has enough space to fit any of the candidates
            if lists[-1]['count']<max_list_size:
                #determine the max amount of users the list can take
                take=min(max_list_size-lists[-1]['count'],len(candidates))
                #determine whether the candidates should go to the twitter lists or bulk lists
                if(is_twitter_list):
                    try:
                        #use the api to add the new users to the list
                        self._twitter.create_list_members(list_id=self._user_lists[-1]['id'],user_id=candidates[:take])
                        #update the size of the list
                        lists[-1]['count']=lists[-1]['count']+take
                    except:
                        #error occurred can not put anything into the list return the remaining number of candidates
                        print ""
                        return candidates
                else:
                    #put users into the last bulk list
                    lists[-1]['ids']+=candidates[:take]
                    #update the bulk list's size
                    lists[-1]['count']=len(self._bulk_lists[-1]['ids'])
                #remove the users we just added
                candidates=candidates[take:]
                #recurse and attempt to fit in more users
                return self.fit_to_lists(candidates,lists,max_list_num,max_list_size,is_twitter_list)
        #either no free list was found or no lists exist
        if(is_twitter_list):
            try:
                #create a new twitter list
                list_id=self._twitter.create_list(name="",mode='private')['id']
                #add it to the crawler data base
                self._user_lists.append({'id':list_id,'count':0})
                #recurse and try to fill the new list
                return self.fit_to_lists(candidates,self._user_lists,max_list_num,max_list_size,is_twitter_list)
            except:
                print "Twitter List could not be created"
        else:
            #calculate how many users we can take into a bulk list
            take=min(max_list_size,len(candidates))
            #create a new bulk list for our users and put them in it
            self._bulk_lists.append({'ids':candidates[:take],'count':take})
            #remove the users we just added
            candidates=candidates[take:]
            #recurse and attempt to fit them into the same or new list
            return self.fit_to_lists(candidates,self._bulk_lists,max_list_num,max_list_size,is_twitter_list)
        #return the remaining users which we could not add to any list
        return candidates
    def __follow_users__(self,candidates):
        try:
            if(candidates):
                #if there are some users remaining see if we have space to follow their timeline without following them
                if len(self._users)< constants.TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS:
                    take=min(constants.TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS-len(self._users),len(candidates))
                    self._users+=[{'id':c['id'],'current_tweet':0} for c in candidates[:take]]
                    candidates=candidates[take:]
            if(candidates):
                #follow all the remaining users which we couldn't find a place for
                for i in range(min(constants.TWITTER_MAX_NUM_OF_REQUESTS_PER_CYCLE,len(candidates))):
                    try:
                        self._twitter.create_friendship(user_id=candidates[i],follow=True)
                    except:
                        print "Could not follow user "+str(candidates[i])
        except:
            print ""
        return candidates

    def __get_friends_and_followers__(self,id,rqs_remaining):
        users=[]
        try:
            #check if we have any get id requests remaining if so get the data and decrement
            if(rqs_remaining[0]>0):
                users+=self._twitter.get_friends_ids(user_id=id)["ids"]
                users+=self._twitter.get_followers_ids(user_id=id)["ids"]
                rqs_remaining[0]-=1
            #check if we have any get list of user requests remaining
            elif(rqs_remaining[1]>0):
                users+=reduce(lambda x:x["id"],self._twitter.get_friends_list(user_id=id)["users"])
                users+=reduce(lambda x:x["id"],self._twitter.get_followers_list(user_id=id)["users"])
                rqs_remaining[1]-=1
        except:
            print ""
        return users

    #attempts to find new accounts to follow
    def explore(self,total_followed):
        candidates=[]
        try:
            #get our suggested categories
            slugs=self._twitter.get_user_suggestions()
            data=self._twitter.verify_credentials()
            #get the people who we are following
            following=self._twitter.get_friends_ids(screen_name=data['screen_name'])
            #get the total number of twitter users that we follow including bulk list users and twitter list users as well as non followed users
            #total_followed=set(following).add(self._users).add(self.get_list_members())
            ff_requests=[15,30]#friends_ids and followers_ids requests remaining
            for s in slugs:
                #get some suggested users in the given category
                users=self._twitter.get_user_suggestions_by_slug(slug=s['name'])['users']
                users=[u['id'] for u in users]
                for u in users:
                    users+=self.__get_friends_and_followers__(u,ff_requests)
                #get the users which we currently do not follow only
                candidates+=list(set(users)-total_followed)
            #try to fit some of the candidates into the twitter lists
            candidates=self.fit_to_lists(candidates,self._user_lists, constants.TWITTER_MAX_NUMBER_OF_LISTS, constants.TWITTER_MAX_LIST_SIZE,True)
            #try to fit some users into the bulk lists
            candidates=self.fit_to_lists(candidates,self._bulk_lists, constants.TWITTER_MAX_NUM_OF_BULK_LISTS,
                                         constants.TWITTER_BULK_LIST_SIZE,False)
            self.__follow_users__(candidates)
        except:
            print "Request Limit on Twitter reached"
        return candidates
    #fetches the crawler's timeline id specifies the id of the last returned tweet, if since is true
    # crawler returns tweets that were posted after the given id
    def fetch_home_timeline(self,task_data):
        data=[]
        max_attempts=15
        current_id=task_data["id"]
        try:
            while max_attempts>0:
                temp_data=[]
                if current_id==0:
                    temp_data+=self._twitter.get_home_timeline()
                    current_id=temp_data[-1]["id"]
                    task_data["id"]=temp_data[0]["id"]
                elif task_data["since"]:
                    temp_data+=self._twitter.get_home_timeline(since_id=current_id)
                    current_id=temp_data[0]["id"]
                    task_data["id"]=current_id
                else:
                    temp_data+=self._twitter.get_home_timeline(max_id=current_id)
                    current_id=temp_data[-1]["id"]
                data+=temp_data
                max_attempts-=1
        except twython.TwythonRateLimitError as e:
            self._wait_for[0]=datetime.datetime.now()
            print e
        return data
    #fetches the specified user's timeline
    def fetch_user_timeline(self,user):
        data=[]
        try:
            data=self._twitter.get_user_timeline(user)
        except twython.TwythonRateLimitError as e:
            self._wait_for[1]=datetime.datetime.now()
            print e
        return data
    #fetches the tweets in the specified list of _users
    def fetch_list_tweets(self,list):
        data=[]
        try:
            data=self._twitter.get_list_statuses(list)
        except twython.TwythonRateLimitError as e:
            self._wait_for[2]=datetime.datetime.now()
            print e
        return data
    #fetches the latest tweets of up to 100 _users
    #as specified in the user_ids list
    def fetch_bulk_tweets(self,user_ids):
        data=[]
        try:
            data=self._twitter.lookup_user(user_ids)
        except twython.TwythonRateLimitError as e:
            self._wait_for[3]=datetime.datetime.now()
            print e
        return data
 #Dim token = "821591210-iYuSCipISYWur43aECxEVFbPXaLIyZz02gy5iJXr"

    def get_trends(self,**kwargs):
        trends=[]
        if('woeid' in kwargs):
            trends=self._twitter.get_place_trends(id=kwargs['woeid'])
        elif('lat' in kwargs and 'long' in kwargs):
            trends=self._twitter.get_closest_trends(lat=kwargs['lat'],long=kwargs['long'])
        else:
            locations=self._twitter.get_available_trends()
            if('location' in kwargs):
                loc=kwargs['location'].lower()
                locations=filter(lambda x:x['country'].lower()==loc or x['name'].lower()==loc or x['countryCode'].lower()==loc,locations)
                locations=(x['woeid'] for x in locations)
                i=0
                for l in locations:
                    if(i== constants.MAX_TWITTER_TRENDS_REQUESTS):
                        break
                    else:
                        trends+=self.get_trends(woeid=l)
                        i+=1
        return trends

#Dim tokenSecret = "i75mvboXg4GLZ3DxjliPibS2C67fFHro07MNgc5n1I"
#Dim consumerKey = "LnPgs7nQZCep40xkQAq5QQ"
#Dim consumerSecret = "i08dNhUJtdNWcFxd7mHYPaw9cVHbQXUw5zlLC3TYJJs"
t=TwitterHandler({'app_key':'532o7CWAK3VbNeXKoBo0YA','app_secret':'coL8NQivDhsnmjWvobvnoFxBjTNcli2UR2RHCCsVFM','oauth_token':'1063077252-YJg2TIFW1ypFblBrHHnPTsRVo1yLv9ZrPEG3YU2','oauth_token_secret':'zyz4D8N5HCLWv4bjrwMe5PWI0TaM0YvhIEQROY2tdmc'},[])
t.explore()