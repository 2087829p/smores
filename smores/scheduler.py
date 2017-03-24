import storage as st
from heapq import *
import minion as m
import handlers
import constants as c
import random
from utils import *
from math import *
import Queue
import time
import os
from collections import deque
__author__ = 'tony petrov'

# task={}
# 'site':'twitter,instagram,blah blah'          - site from which data will be retrieved
# 'op':1,2,3,...                                - code of the operation performed refers to the fetch function that the crawler is executing in this task
# 'data':[2032,321,23213,123]                   - contains ids/names/lists of users the minion should get data for
# 'fetch':Handler.f                             - data fetching function from a social media handler
# 'store':f(x)                                  - address of function to which the data should be returned
# 'timeout':213123                              - tells the scheduler that the task is unavailable for execution until the timestamp==time.now()


DB_CONTEXT_SWITCH_TIMEOUT = 86400  # every day new db
COLLECTION_CONTEXT_SWITCH_TIMEOUT = 3600  # every hour (aka cycle) new collection of docs


class RankingFilter(st.Filter):
    def __init__(self, service, store, filters, classifier=PERCEPTRON_CLASSIFIER):
        super(RankingFilter, self).__init__(service, store, filters)
        self._active_users = {}
        self._total_tags = 0
        self._hot_topics = {}
        self._last_updated = time.time()
    # try to load a previously trained classifier
        self._classifier = st.load_data(RANKING_FILTER_CLASSIFIER)
        self._training_users = []
        self._training_topics = []
    # check if we have trained a classifier before and if yes then load it
        self._topic_classifier = st.load_data(RANKING_FILTER_TOPIC_CLASSIFIER) \
            if os.path.exists(st.__abs_path__(RANKING_FILTER_TOPIC_CLASSIFIER)) \
            else KMeanClassifier()
        if not self._classifier:
            if classifier == PERCEPTRON_CLASSIFIER:
                self._classifier = NeuralNetwork(5, 1)
            elif classifier == DEEP_NEURAL_NETWORK_CLASSIFIER:
                self._classifier = NeuralNetwork(5, 1, True)
                for _ in range(3):
                    self._classifier.add_hidden_layer(50)
            elif classifier == K_MEANS_CLASSIFIER:
                self._classifier = KMeanClassifier()

    def __train_and_rank__(self, now):
        influential_users = []
        if isinstance(self._classifier, NeuralNetwork):	#if we are using a neural network single/multi layer
            for k in self._active_users:
                u = self._active_users[k]
                # fit tslp in window and then cast the window size in range 0 to 1
                # then increase the weight of smaller tslp's since shorter time means more active user!
                u['tslp'] = 1.0 - (np.clip(fit_in_range(0.0,RUNNING_CYCLE,u['tslp']),0,1))
                influential_users.append((float(self._classifier.predict(
                    [u['tslp'], u['followers'], u['friends'],  u['mentions'], u['post_frq']])[0]), k))
        else:
        # not using a neural network use k-means
            influential_users = [(self._classifier.predict(np.array(self._active_users[u]['series'])), u) for u in
                                 self._active_users.keys()]
        max_number_of_tweets_per_cycle = 500 # max number of tweets to be stored for future training
        if self._training_topics:
            topics = self._training_topics
            max_number_training_samples = 50
            take = min(len(topics) / 4, max_number_training_samples)
            # split topics into 2 sets positive and negative
            pos_t = []
            neg_t = []
            for t in topics:
                if t in self._hot_topics:
                    pos_t.append(t)
                else:
                    neg_t.append(t)
            pos_t = pos_t[:take]
            neg_t = neg_t[:take]
            #====================================================
            for i in xrange(min(len(pos_t),len(neg_t))):
                try:
                    with self._lock:
                        self._topic_classifier.train(self._training_topics[pos_t[i]]['series'], 1)
                        self._topic_classifier.train(self._training_topics[neg_t[i]]['series'], 0)
                except Exception as e:
                    print "Error while training classifier : %s" % e.message
        hot_topics = [(self._topic_classifier.predict(self._hot_topics[k]['series']), k) for k in
                          self._hot_topics.keys()]
        self._training_topics = self._hot_topics
        out = (hot_topics, influential_users)
    # randomly choose users for training set
        samples = random.sample(out[1], min(len(out[1]), max_number_of_tweets_per_cycle))
        if self._training_users:
            epochs = 80
            for s in self._training_users.keys():
                u = self._training_users[s]
                if isinstance(self._classifier, NeuralNetwork):
                    with self._lock:
                        self._classifier.train(
                        [u['tslp'], u['followers'], u['friends'], u['mentions'],
                                 u['post_frq']],
                        [1.0 if s in self._active_users else 0.0],epochs)
                else:
                    with self._lock:
                        self._classifier.train(u['series'], 1.0 if s in self._active_users else 0.0)
        self._training_users = {s[1]: self._active_users[s[1]] for s in samples}
        self._hot_topics = {}
        self._last_updated = now
        self._active_users = {}
        return out

    def process(self, data):
        now = time.time()
        cycle = int(now - self._last_updated)	# which cycle we are at since the last time we've trained
        if now > self._last_updated + c.RANK_RESET_TIME: # check if it's time to train if yes then train
            return self.__train_and_rank__(now)
        if isinstance(data,dict):   # can't iterate over a dict so cast it to a list
            data = [data]
        for t in data:
            if 'user' not in t or 'id' not in t.get('user',{}):
                continue
            user = self._active_users.setdefault(t['user']['id'],
                                                 dict(tslp=time.time(), followers=0, friends=0, total_posts=0, mentions=0,
                                                    post_frq=0, series=[1.0 for _ in xrange(RUNNING_CYCLE)]))
            created = get_tweet_timestamp(t)
            scaling_factor = 19     # maximum size of a 64 bit int like the one that Twitter uses
            user["tslp"] = created - user.get('tslp',now) # calculate the time since last post
            # scale friends and followers to fit range 0 to 1 the higher the number of friends/followers the closer to 1
            user["followers"] = fit_in_range(0, scaling_factor, log10(max(1,t["user"].get("followers_count",1))))
            user["friends"] = fit_in_range(0, scaling_factor,log10(max(1,t["user"].get("friends_count",1))))
            #=================================================================================================
            user["total_posts"] += 1
            user["post_frq"] = user["total_posts"] / float(RUNNING_CYCLE)
            user['series'][ max(0,min(cycle, int(now - created)))] += 1.0
            entities = t.get('entities',{})
            if "hashtags" in entities:
                for h in entities["hashtags"]:
                    tag = h.get("text","")
                    if not all_ascii(tag):
                        continue            # tweet is probably not in English so skip it
                    topic = self._hot_topics.setdefault(tag, dict(series=[1.0 for _ in xrange(RUNNING_CYCLE)],
                                                           count=0))
                    topic['series'][max(0,min(cycle, int(now - created)))] += 1.0
                    topic["count"] += 1
            if 'user_mentions' in entities:
                for m in entities['user_mentions']:
                    u = self._active_users.setdefault(m["id"], dict(tslp=time.time(), followers=0, friends=0,
                                                                    total_posts=0, mentions=0, post_frq=0,
                                                                    series=[1.0 for _ in xrange(RUNNING_CYCLE)]))
                    u['mentions'] += 1
        return None

    def interrupt(self):
        with self._lock:
            st.save_data(self._classifier, RANKING_FILTER_CLASSIFIER)
            st.save_data(self._topic_classifier, RANKING_FILTER_TOPIC_CLASSIFIER)
        super(RankingFilter, self).interrupt()



class Scheduler:
    def __init__(self, **kwargs):
        self._minions = []
        self._sites = kwargs.get('sites', ['twitter'])
        self._plugins = kwargs.get('plugins', [])
        self._use = kwargs.get('use', TWITTER_CYCLE_HARVESTER)
        self._classifier = kwargs.get('classifier',PERCEPTRON_CLASSIFIER)
        import multiprocessing
        cores = multiprocessing.cpu_count()
        self._thread_num = max(1, (cores - len(self._plugins)) / 2) if kwargs.get('multicore', False) else 1
        self._lock = threading.Lock()
        self._handlers = []
        login = filter(lambda x: x if x['site'] == 'twitter' else None,st.read_login(TWITTER_CREDENTIALS))
        proxies = st.read_login(PROXY_LOCATION)
        # TODO ADD SOME PROXY CHECK IF ALIVE FUNCTION
        ix = 0
        for l in login:
            if l['site'] == 'twitter':
                if len(proxies) > 0:
                    proxy = {'proxies': proxies.pop()}
                    t = handlers.TwitterHandler(l, False, id=ix, client_args=proxy, scheduler=self)
                    self._handlers.append(t)
                    ix += 1
                else:
                    t = handlers.TwitterHandler(l, False, id=ix, scheduler=self)
                    self._handlers.append(t)
                    ix += 1
                    break  # we ran out of proxies so just exit
        c.TWITTER_ACCOUNTS_COUNT = ix
        self._trends = kwargs.get('trends', {})
        self._target_queue = dict()
        self._target_queue['tumblr_tags'] = kwargs.get('tumblr_tags', [])
        self._target_queue['fb_users'] = kwargs.get('fb_users', [])
        self._target_queue['blogs'] = kwargs.get('blogs', [])
        if not self._trends or contains_locations(self._trends):
            self._trends = self.__get_top_n_trends__(-1,True)
        if c.TESTING:
            self._predefined_store = False
            self._store = None
            self._thread_num += cores - (self._thread_num + len(self._plugins))
        else:
            if 'storage' in kwargs.keys():
                self._storages = kwargs['storage']
                self._predefined_store = True
                if not kwargs['storage']:
                    import warnings
                    warnings.warn("No storage system is specified this may lead to loss of data",Warning)
                    # double the number of crawler threads we have no storage
                    self._thread_num += self._thread_num if kwargs.get('multicore', False) else 0
                    return
            else:
                if 'ip' not in kwargs.keys() and 'port' not in kwargs.keys():
                    raise ValueError('IP and port of the MongoDB server must be specified')
                self._storage = st.StorageSystem(kwargs['ip'], kwargs['port'], self._thread_num)
                self._store = self._storage.write
                self._predefined_store = False
            self._thread_num += 1 if kwargs.get('multicore', False) else 0

        

    def add_filters(self, filters):
        """add new plugins to the beginning of the toolchain"""
        self._plugins += filters

    def start(self):
        """Starts the scheduler, all minions and databases"""
        self._timers = []
        if not c.TESTING:
            if not self._predefined_store:
        # add times to change the name of the db after 1 day and the name of the collection after each cycle
                self._timers.append(CrawlTimer(COLLECTION_CONTEXT_SWITCH_TIMEOUT,
                                               self._storage.switch_collection_context))
                self._timers.append(CrawlTimer(DB_CONTEXT_SWITCH_TIMEOUT, self._storage.switch_db_context))

            else:
                self._timers.append(
                    CrawlTimer(DB_CONTEXT_SWITCH_TIMEOUT, None))
            non_twitter = filter(lambda x: x if not isinstance(x, handlers.TwitterHandler) else None, self._handlers)
            if non_twitter:
                timer = self._timers[-1]
                for i in xrange(len(non_twitter)):	# add a function to reset the quotas of tumblr and facebook after 1 hour
                    timer.add_function(non_twitter[i].reset_daily_requests)
        if self._use == TWITTER_STREAMING_BUCKET_MODEL:
            self.__setup_streamer__(self._trends)
        elif self._use == TWITTER_STREAMING_HARVESTER_NON_HYBRID:
            self.__setup_streamer__(self._trends)
            self.__setup_minions__()
        elif self._use == TWITTER_HYBRID_MODEL:
            self._plugins.append(RankingFilter(TWITTER_PLUGIN_SERVICE, self.__update_future_queue__, [],self._classifier))
            self.__setup_streamer__(self._trends)
            self.__setup_minions__()
        else:
            self.__setup_minions__()
        self._cycles = [0 for _ in xrange(TOTAL_TASKS)] # used for debug purposes
        print "Crawling with %d minions" % len(self._minions)
        for mn in self._minions:
            mn.start()
        for p in self._plugins:
            p.start()
        if not TESTING and self._timers:
            for t in self._timers:
                t.start()

    def terminate(self):
        """Terminates all tasks and closes all database connections"""
        for mn in self._minions:
            mn.interrupt()
        if self._plugins:
            for p in self._plugins:
                p.interrupt()
        if not c.TESTING:
            if not self._predefined_store:
                self._storage.shutdown()
            for t in self._timers:
                t.stop()

    def __setup_minions__(self):
        self._tasks = self.__prepare_work__()
        unique_ops = len(set([t[1]['op'] for t in self._tasks.queue]))
        if (self._use == TWITTER_HYBRID_MODEL or self._use == TWITTER_STREAMING_HARVESTER_NON_HYBRID) and not c.TESTING and self._thread_num<2:
            #if we are using both minions and streaming add an extra minion
            # this is done to avoid stalling due to too low thread count and getting stuck in slow ops
            self._thread_num += 1
        self._thread_num = min(self._thread_num, unique_ops)
        for i in xrange(self._thread_num):
            task = self._tasks.get_nowait()[1]
            self._tasks.task_done()
            self._minions.append(m.Minion(task, lock=self._lock, scheduler=self))


    def __setup_streamer__(self, trend_data):
        login = [l for l in st.read_login(TWITTER_CREDENTIALS) if l['site'] == 'twitter']
        for i in xrange(len(login)):
            login[i]['id'] = i
        serv = TWITTER_STREAMING_PLUGIN_SERVICE if self._use == TWITTER_STREAMING_BUCKET_MODEL else TWITTER_PLUGIN_SERVICE
        plugins = [p for p in self._plugins if p._for == serv]
        store = self._store if not self._predefined_store else self._storages
        t = {'site': 'twitter', 'op': TASK_FETCH_STREAM, 'data': trend_data, 'fetch': None, 'store': store,
             'plugins': plugins}

        self._minions.append(m.Streamion(login, t, lock=self._lock, scheduler=self))

    def __prepare_twitter__(self, tasks):
        """Generates a queue of tasks for the Twitter cycle harvester model"""
        # get the plugins for the twitter harvester service or twitter service
        service = TWITTER_HARVESTER_PLUGIN_SERVICE if self._use == TWITTER_CYCLE_HARVESTER else TWITTER_PLUGIN_SERVICE
        twitter_plugins = [p for p in self._plugins if p._for == service]
        # ===================load data=============
        remaining_users = st.load_data(TWITTER_CANDIDATES_STORAGE)
        remaining_users = remaining_users if remaining_users else []
        bulk_lists = st.load_data(TWITTER_BULK_LIST_STORAGE)
        lists = st.load_data(TWITTER_LIST_STORAGE)
        users = st.load_data(TWITTER_USER_STORAGE)
        timeline = st.load_data(TWITTER_WALL_STORAGE)
        #=========================================
        if not timeline:
            timeline = {'id': 0}
        # split ids into lists of the correct size for the given task
        blg = split_into(bulk_lists, TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE)
        bulk_lists = [l for l in blg]
        lg = split_into(lists, TWITTER_MAX_NUMBER_OF_LISTS)
        lists = [l for l in lg]
        ug = split_into(users, TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS)
        users = [l for l in ug]
        #============================================================
        store = self._store if not self._predefined_store else self._storages

        # build task data queues
        self._target_queue[TASK_BULK_RETRIEVE] = deque(bulk_lists)
        self._target_queue[TASK_FETCH_USER] = deque(users)
        self._target_queue[TASK_FETCH_LISTS] = deque(lists)
        self._target_queue[TASK_UPDATE_WALL] = deque([timeline])
        self._target_queue[TASK_EXPLORE] = deque([remaining_users])
        # ============================
        twitters = filter(lambda x: isinstance(x, handlers.TwitterHandler), self._handlers)
        for i in range(len(twitters)):          # for each twitter account create a new task
            t = twitters[i]
            if not c.COLLECTING_DATA_ONLY:
                tasks.put((0, {'site': 'twitter', 'op': TASK_EXPLORE,
                            'data': {'remaining': remaining_users,
                                     'bulk_lists': flatten(bulk_lists),
                                     'total_followed': flatten(users),
                                     'user_lists': flatten(lists),
                                     },
                            'fetch': t.explore,
                            'store': st.save_candidates,
                            'plugins': twitter_plugins,
                            'acc_id': t.id}))
            if not c.EXPLORING:
                tasks.put((0, {'site': 'twitter', 'op': TASK_UPDATE_WALL,
                               'data': timeline, 'fetch': t.fetch_home_timeline,
                               'store': store, 'plugins': twitter_plugins,
                               'acc_id': t.id}))
                tasks.put((0, {'site': 'twitter', 'op': TASK_BULK_RETRIEVE,
                               'data': bulk_lists[i] if len(bulk_lists) > i else [],
                               'fetch': t.fetch_bulk_tweets, 'store': store,
                               'plugins': twitter_plugins,
                               'acc_id': t.id}))
                tasks.put((0, {'site': 'twitter', 'op': TASK_FETCH_LISTS,
                               'data': lists[i] if len(lists) > i else [], 'fetch': t.fetch_list_tweets,
                               'store': store, 'plugins': twitter_plugins, 'acc_id': t.id}))
                tasks.put((0, {'site': 'twitter', 'op': TASK_FETCH_USER,
                               'data': users[i] if len(users) > i else [], 'fetch': t.fetch_user_timeline,
                               'store': store, 'plugins': twitter_plugins, 'acc_id': t.id}))
                tasks.put((0, {'site': 'twitter', 'op': TASK_TWITTER_SEARCH,
                              'data': dict(keywords=self.__get_top_n_trends__(-1)), 'fetch': t.search,
                              'store': store, 'plugins': twitter_plugins, 'acc_id': t.id}))
        return tasks

    def __prepare_tumblr__(self, tasks, login):
        t = handlers.TumblrHandler(login)
        self._handlers.append(t)
        tumblr_plugins = [p for p in self._plugins if
                          p._for == TUMBLR_PLUGIN_SERVICE or p._for == CRAWLER_PLUGIN_SERVICE]
        store = self._store if not self._predefined_store else self._storages
        self._target_queue[TASK_GET_DASHBOARD] = deque([])
        self._target_queue[TASK_GET_TAGGED] = deque([])
        self._target_queue[TASK_GET_BLOG_POSTS] = deque([])
        tasks.put(0, {'site': 'tumblr', 'op': TASK_GET_DASHBOARD,
                      'data': [], 'fetch': t.get_dashboard,
                      'store': store, 'plugins': tumblr_plugins})
        tasks.put(0, {'site': 'tumblr', 'op': TASK_GET_TAGGED,
                      'data': [], 'fetch': t.get_post_with_tag,
                      'store': store, 'plugins': tumblr_plugins})
        tasks.put(0, {'site': 'tumblr', 'op': TASK_GET_BLOG_POSTS,
                      'data': [], 'fetch': t.get_blog_posts,
                      'store': store, 'plugins': tumblr_plugins})

    def __prepare_facebook__(self, tasks, login):
        f = handlers.FacebookHandler(login)
        self._handlers.append(f)
        facebook_plugins = [p for p in self._plugins
                            if p._for == FACEBOOK_PLUGIN_SERVICE or p._for == CRAWLER_PLUGIN_SERVICE]
        store = self._store if not self._predefined_store else self._storages
        self._target_queue[TASK_GET_FACEBOOK_WALL] = deque([])
        self._target_queue[TASK_FETCH_FACEBOOK_USERS] = deque([])
        tasks.put(0, {'site': 'facebook', 'op': TASK_GET_FACEBOOK_WALL,
                      'data': [], 'fetch': f.get_my_wall,
                      'store': store, 'plugins': facebook_plugins})
        tasks.put(0, {'site': 'facebook', 'op': TASK_FETCH_FACEBOOK_USERS,
                      'data': [], 'fetch': f.get_posts_for_users,
                      'store': store, 'plugins': facebook_plugins})

    def __prepare_work__(self):
        """Prepares the crawler tasks"""
        tasks = Queue.PriorityQueue()
        login = st.read_login(TWITTER_CREDENTIALS)
        for s in self._sites:
            if s == 'twitter':
                self.__prepare_twitter__(tasks)
            if s == 'tumblr':
                self.__prepare_tumblr__(tasks, filter(lambda x: x if x['site'] == 'tumblr' else None, login))
            if s == 'facebook':
                self.__prepare_facebook__(tasks, filter(lambda x: x if x['site'] == 'facebook' else None, login))
        return tasks

    def __update_future_queue__(self, data):
        """Update the queue for the hybrid model"""
        if not data:
            return
        users = data[1]
        topics = data[0]
        self._target_queue['users'] = users
        self._trends = topics 

    def __get_top_n_accounts__(self, n):
        ret = nlargest(n, self._target_queue["users"])
        self._target_queue['users'].sort(reverse=True)
        self._target_queue["users"] = self._target_queue["users"][n:]
        return [i[1] for i in ret]

    def __get_top_n_trends__(self, n,SYS_INIT=False):
        """Retrieves the top n most popular trends"""
        if self._use == TWITTER_HYBRID_MODEL and not SYS_INIT:
            # we're using the hybrid model and we're no initializing the system so get topics from the predicted topics
            if n == -1:
                return [i[1] for i in self._trends]
            ret = nlargest(n, self._trends)
            self._trends.sort(reverse=True)
            self._trends = self._trends[n:]
            return [i[1] for i in ret]
        else:
            try:
                if c.TIME_TO_UPDATE_TRENDS < time.time(): # check if we should refresh our topic list
                    twitter = filter(lambda x: isinstance(x, handlers.TwitterHandler), self._handlers)[0]
                    # if a location was specified in the trends tell the handler if not just request
                    self._trends = twitter.get_trends(self._trends) if contains_locations(self._trends) \
                        else twitter.get_trends(dict())
                    c.TIME_TO_UPDATE_TRENDS = time.time() + RUNNING_CYCLE
                if n == -1:
                    return self._trends
        # get the number of topics requested and remove them from the queue/list
                out = self._trends[:n]
                self._trends = self._trends[n:]
        #================================================================
                return out
            except:
                pass
        return []

    def __get_data__(self, task):
        if self._use == TWITTER_HYBRID_MODEL and self._target_queue['users'] and task in [TASK_FETCH_USER,
                                                                                          TASK_BULK_RETRIEVE]:
            if task == TASK_BULK_RETRIEVE:
                if not self._target_queue[task]:
                    return [self.__get_top_n_accounts__(TWITTER_BULK_LIST_SIZE) for _ in
                            xrange(TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE)]
                predicted = [{'ids':self.__get_top_n_accounts__(TWITTER_BULK_LIST_SIZE)} for _ in
                             xrange(int(TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE * c.PARTITION_FACTOR))]
                normal = self._target_queue[task].pop()     # get a sample of users from the database
                self._target_queue[task].appendleft(normal) # put the sample at the end for future use
                if len(normal) == 0:
                    return predicted
    # return a mix of predicted users and users from the db to avoid pollution of data
                return predicted + random.sample(normal,
                                                 min(len(normal)/2,     #needed to ensure that the sample is never larger than the population
                                                     TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE - len(predicted)))
            elif task == TASK_FETCH_USER:
        # get predicted users up to the specified partition
                predicted = self.__get_top_n_accounts__(int(TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS * c.PARTITION_FACTOR))
                normal = self._target_queue[task].pop()     # get a sample of users from the database
                self._target_queue[task].appendleft(normal) 
                if len(normal) == 0:
                    return predicted
                return predicted + random.sample(normal,
                                                 min(len(normal)/2,     #needed to ensure that the sample is never larger than the population
                                                     TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE - len(predicted)))
        else:
            if self._target_queue[task]:
                # if we have data give it
                return self._target_queue[task].pop()
            else:
                # no data check if explorer has found anything yet
                if task == TASK_BULK_RETRIEVE:
                    lists = st.load_data(TWITTER_BULK_LIST_STORAGE)
                    if not lists:
                        return []
                    lst = split_into(lists, TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE)
                    self._target_queue[TASK_BULK_RETRIEVE] = deque([l for l in lst])
                elif task == TASK_FETCH_LISTS:
                    lists = st.load_data(TWITTER_LIST_STORAGE)
                    if not lists:
                        return []
                    lst = split_into(lists, TWITTER_MAX_NUMBER_OF_LISTS)
                    self._target_queue[TASK_FETCH_LISTS] = deque([l for l in lst])
        #=====================================================================
                return self._target_queue[task].pop()
        return []

    def __put_data__(self, task, data):
        with self._lock:
            self._target_queue[task].appendleft(data)

    def request_work(self, task):
        """Request a new task once the old one is finished"""       
        if task['site'] != 'sleep':
            if not 'timeout' in task:
                task['timeout'] = time.time() + (RUNNING_CYCLE if task['site'] == 'twitter'
                                                 else DEFAULT_SOCIAL_MEDIA_CYCLE)
            self._tasks.put((task['timeout'], task))
            with self._lock:
                self._cycles[task['op']] += 1
            if task['op'] != TASK_TWITTER_SEARCH:
                self.__put_data__(task['op'], task['data'])            
        if not self._tasks.queue:
            # No data yet so check again in 5 seconds
            return {'site': 'sleep', 'time': 5}
        top = self._tasks.queue[0]
        # Check if task has ever been executed if not then just give it to the worker
        if top[0] == 0:
            t = self._tasks.get()[1]
            self._tasks.task_done()
            return t
        now = time.time()
        # Check if the timeout of the next task has expired
        data = []
        t = {}
        while not data:
            if top[0] > now:
                wait = top[0] - now
                # No then sleep til ready
                return dict(site='sleep', time=wait)
            # Yes then get data for the task
            t = self._tasks.get()[1]
            if t['op'] == TASK_EXPLORE:
                t['data'] = st.load_explorer_data()
                break
            if t['op'] == TASK_UPDATE_WALL:
                t['data'] = st.load_data(TWITTER_WALL_STORAGE)
                break
            if t['op'] == TASK_TWITTER_SEARCH:
                t['data'] = {'keywords':self.__get_top_n_trends__(-1)}
                break
            # try to get data for the task
            data = self.__get_data__(t['op'])
            if data:
                # if we have data for the task assign and exit
                t['data'] = data
            else:
                # if we have no data for the task then skip and try next task in queue
                self._tasks.put((DEFAULT_SOCIAL_MEDIA_CYCLE + now, task))
            top = self._tasks.queue[0]
        if t['site'] == 'tumblr':
            tumblrs = filter(lambda x: isinstance(x, handlers.TumblrHandler), self._handlers)
            for tb in tumblrs:
                tb.reset_requests()
        elif t['site'] == 'facebook':
            fbs = filter(lambda x: isinstance(x, handlers.FacebookHandler), self._handlers)
            for f in fbs:
                f.reset_requests()
        self._tasks.task_done()
        return t
