__author__ = 'tony petrov'

import datetime as dt
from smores import storage as st
from heapq import *
import minion as m
import handlers
from constants import *
import random
from utils import *
from math import *
import Queue
import time
# task={}
# 'site':'twitter,instagram,blah blah'          - site from which data will be retrieved
# 'op':1,2,3,...                                - code of the operation performed refers to the fetch function that the crawler is executing in this task
# 'data':[2032,321,23213,123]                   - contains ids/names/lists of users the minion should get data for
# 'fetch':Handler.f                             - data fetching function from a social media handler
# 'store':f(x)                                  - address of function to which the data should be returned
# 'timeout':213123                              - tells the scheduler that the task is unavailable for execution until the timestamp==time.now()
TASK_EXPLORE = 0
TASK_BULK_RETRIEVE = 1
TASK_FETCH_LISTS = 2
TASK_FETCH_USER = 3
TASK_UPDATE_WALL = 4
TASK_FETCH_STREAM = 5
TOTAL_TASKS = 6
PARTITION_FACTOR = 0.5
DB_CONTEXT_SWITCH_TIMEOUT = 86400  # every day new db
COLLECTION_CONTEXT_SWITCH_TIMEOUT = 3600  # every hour (aka cycle) new collection of docs

class RankingFilter(st.Filter):
    def __init__(self, service, store, filters):
        super(RankingFilter,self).__init__(service,store,filters)
        self._influential_users = {}
        self._total_tags=0
        self._hot_topics = {}
        self._last_updated = time.time()
        self._classifier = st.load_data(RANKING_FILTER_CLASSIFIER)
        self._training_users = []
        self._training_topics = []
        self._topic_classifier = KMeanClassifier()
        if not self._classifier:
            self._classifier = NeuralNetwork(6,1)

    def process(self, data):
        now = time.time()
        cycle = int(now-self._last_updated)
        if now>self._last_updated + RANK_RESET_TIME:
            influential_users = [(self._classifier.predict(np.array(self._influential_users[u].values())),u) for u in self._influential_users.keys()]
            hot_topics = []
            if self._training_topics:
                topics = sorted(self._hot_topics,key=self._hot_topics.get)
                take = min(len(topics)/4,50)
                pos_t = topics[-take:]
                neg_t = topics[:take]
                for i in range(take):
                    self._topic_classifier.train(self._training_topics[pos_t[i]]['series'],1)
                    self._topic_classifier.train(self._training_topics[neg_t[i]]['series'],0)
                hot_topics = [(self._topic_classifier.predict(self._hot_topics[k]['series']),k) for k in self._hot_topics.keys()]
            self._training_topics = self._hot_topics
            out = (hot_topics,influential_users)
            samples = random.sample(out[1],max(len(out[1]),500))
            if self._training_users:
                for s in self._training_users.keys():
                    self._classifier.train(np.array(self._training_users[s].values()),
                                           np.array([1.0 if s in self._influential_users else 0.0]))
            self._training_users = {s:self._influential_users[s] for s in samples}
            self._hot_topics = {}
            self._last_updated = now
            self._influential_users = {}
            return out
        for t in data:
            user = self._influential_users.get(t["id"],dict(tslp=time.time(),followers=0,friends=0,total_posts=0,mentions=0,post_frq=0))
            created = time.mktime(time.strptime(t["created_at"],"%a %b %d %H:%M:%S +0000 %Y"))
            user["tslp"] =  created - user.get("tslp",0)
            user["followers"] = fit_in_range(0,19,log10(t["user"]["followers_count"])) if "user" in t and "followers_count" in t["user"] else 0
            user["friends"] = fit_in_range(0,19,t["user"]["friends_count"]) if "user" in t and "friends_count" in t["user"] else 0
            user["total_posts"] +=  1
            user["post_frq"] = user["total_posts"] / float(RUNNING_CYCLE)
            entities = t['entities']
            if "hashtags" in entities:
                for h in entities["hashtags"]:
                    tag = h["text"]
                    topic = self._hot_topics.get(tag,dict(series=[0.0 for i in range(RUNNING_CYCLE)],count=0))#dict(count=0,likes=0,rts=0))
                    topic['series'][min(cycle,int(created-now))] += 1.0
                    #user['tags'] = user.setdefault('tags',set()).add(tag)
                    topic["count"] += 1
                    #topic["likes"] += t["favorite_count"]
                    #topic["rts"] += t["retweet_count"]
                    #self._total_tags += 1
            if 'user_mentions' in entities:
                for m in entities['user_mentions']:
                    u = self._influential_users.get(m["id"],{})
                    u['mentions'] +=  1
        return None



class Scheduler:
    def __init__(self, **kwargs):
        import multiprocessing
        self._thread_num = 1 #max(1,multiprocessing.cpu_count()/2)
        self._minions = []
        self._sites = kwargs['sites'] if 'sites' in kwargs.keys() else ['twitter']
        self._plugins = kwargs['plugins'] if 'plugins' in kwargs.keys() else []
        self._lock = threading.Lock()
        self._trends = kwargs['trends'] if 'trends' in kwargs.keys() else []
        self._twitter = []
        if TESTING:
            self._predefstore = False
            self._store = lambda x: x
        else:
            if 'storage' in kwargs.keys():
                self._storages = kwargs['storage']
                self._predefstore = True
            else:
                if 'ip' not in kwargs.keys() and 'port' not in kwargs.keys():
                    raise ValueError('IP and port of the MongoDB server must be specified')
                self._storage = st.StorageSystem(kwargs['ip'], kwargs['port'], self._thread_num)
                self._store = self._storage.write
                self._predefstore = False
        self._use = kwargs['use'] if 'use' in kwargs else 'minions'
        self._target_queue = {}
        # self.start()

    def add_filters(self, filters):
        'add new plugins to the beginning of the toolchain'
        self._plugins += filters

    def start(self):
        'Starts the scheduler, all minions and databases'
        self._timers = []
        if not TESTING:
            if not not self._predefstore:
                self._timers.append(CrawlTimer(DB_CONTEXT_SWITCH_TIMEOUT, self._storage.switch_db_context))
                self._timers.append(CrawlTimer(COLLECTION_CONTEXT_SWITCH_TIMEOUT,
                                               self._storage.switch_collection_context))
            else:
                for db in self._storages.keys():
                    self._timers.append(
                        CrawlTimer(DB_CONTEXT_SWITCH_TIMEOUT, self._storages[db].switch_db_context))
        if self._use == TWITTER_STREAMING_BUCKET_MODEL:
            self.__setup_streamer__(self._trends)
        elif self._use == TWITTER_HYBRID_MODEL:
            self._plugins=[RankingFilter(TWITTER_PLUGIN_SERVICE,self.__update_future_queue__,[])]
            self.__setup_streamer__(self._trends)
            self.__setup_minions__()
        else:
            self.__setup_minions__()
        self._cycles = [0 for i in range(TOTAL_TASKS)]
        for mn in self._minions:
            mn.start()
        for p in self._plugins:
            p.start()
            # mn.join()
        if not TESTING:
            for t in self._timers:
                    t.start()

    def terminate(self):
        'Terminates all tasks and closes all database connections'
        # ======replace this with a custom timer class if possible===
        # ref:http://stackoverflow.com/questions/9812344/cancellable-threading-timer-in-python

        # ===========================================================
        for mn in self._minions:
            mn.interrupt()
        for p in self._plugins:
            p.interrupt()
        if not TESTING:
            if not self._predefstore:
                self._storage.shutdown()
            for t in self._timers:
                t.stop()


    def __setup_minions__(self):
        self._tasks = self.__prepare_work__()
        print [v['op'] for v in self._tasks.queue]
        unique_ops = len(set([t['op'] for t in self._tasks.queue]))
        self._thread_num = min(self._thread_num, unique_ops)
        for i in range(self._thread_num):
            task = self._tasks.get_nowait()
            self._tasks.task_done()
            self._timeouts[task['acc_id']][task['op']] = dt.datetime.now() + dt.timedelta(
                minutes=TWITTER_CYCLE_DURATION)
            self._minions.append(m.Minion(task, lock=self._lock, scheduler=self))
            # self._tasks.put_nowait(task)

    def __setup_streamer__(self, trend_data):
        login = st.read_login(TWITTER_CREDENTIALS)
        serv = TWITTER_PLUGIN_SERVICE if self._use == TWITTER_HYBRID_MODEL else TWITTER_STREAMING_PLUGIN_SERVICE
        plugins = [p for p in self._plugins if p == serv]
        store = self._store if not self._predefstore else self._storages['stream'].write
        t = {'site': 'twitter', 'op': TASK_FETCH_STREAM, 'data': trend_data, 'fetch': None, 'store': store,
             'plugins': plugins}
        self._minions.append(m.Streamion(login, t, lock=self._lock, scheduler=self))


    def __prepare_twitter__(self, tasks):
        'Generates a queue of tasks for the Twitter cycle harvester model'
        login = st.read_login(TWITTER_CREDENTIALS)
        proxies =st.read_login(PROXY_LOCATION)
        # TODO ADD SOME PROXY CHECK IF ALIVE FUNCTION
        ix = 0
        for l in login:
            if l['site'] == 'twitter':
                if len(proxies) > 0:
                    proxy = {'proxies': proxies.pop()}
                    t = handlers.TwitterHandler(l, False, id=ix, client_args=proxy)
                    self._twitter.append(t)
                    ix += 1
                else:
                    t = handlers.TwitterHandler(l, False, id=ix)
                    self._twitter.append(t)
                    ix += 1
                    break  # we ran out of proxies so just exit

        self._timeouts = [[dt.datetime(1970, 1, 1) for j in range(TOTAL_TASKS)] for i in range(ix)]
        serv = TWITTER_PLUGIN_SERVICE if self._use == TWITTER_HYBRID_MODEL else TWITTER_MODEL_PLUGIN_SERVICE
        twitter_plugins = [p for p in self._plugins if p._for == serv]
        remaining_users = st.load_data(TWITTER_CANDIDATES_STORAGE)
        remaining_users = remaining_users if remaining_users else [0]
        bulk_lists = st.load_data(TWITTER_BULK_LIST_STORAGE)
        lists = st.load_data(TWITTER_LIST_STORAGE)
        users = st.load_data(TWITTER_USER_STORAGE)
        timeline = st.load_data(TWITTER_WALL_STORAGE)
        if not timeline:
            timeline = {'id': 0}
        # return tasks
        blg = split_into(bulk_lists, TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE)
        bulk_lists = [l for l in blg]
        lg = split_into(lists, TWITTER_MAX_NUMBER_OF_LISTS)
        lists = [l for l in lg]
        ug = split_into(users, TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS)
        users = [l for l in ug]
        store = self._store if not self._predefstore else self._storages['model'].write
        from collections import deque
        self._target_queue[TASK_BULK_RETRIEVE] = deque(bulk_lists)
        self._target_queue[TASK_FETCH_USER] = deque(users)
        self._target_queue[TASK_FETCH_LISTS] = deque(lists)
        self._target_queue[TASK_UPDATE_WALL] = deque([timeline])
        self._target_queue[TASK_EXPLORE] = deque([remaining_users])
        for i in range(len(self._twitter)):
            t = self._twitter[i]
            tasks.put((0,{'site': 'twitter', 'op': TASK_EXPLORE,
                                                  'data': {'remaining': remaining_users,
                                                           'bulk_lists': bulk_lists,
                                                           'total_followed': users,
                                                           'user_lists': lists,
                                                  },
                                                  'fetch': t.explore,
                                                  'store': st.save_candidates,
                                                  'plugins': twitter_plugins,
                                                  'acc_id': t.id}))
            tasks.put((0,{'site': 'twitter', 'op': TASK_UPDATE_WALL,
                                           'data': timeline, 'fetch': t.fetch_home_timeline,
                                           'store': store, 'plugins': twitter_plugins,
                                           'acc_id': t.id}))
            tasks.put((0,{'site': 'twitter', 'op': TASK_BULK_RETRIEVE,
                                                      'data': bulk_lists[i] if len(bulk_lists)>i else [],
                                                      'fetch': t.fetch_bulk_tweets, 'store': store,
                                                      'plugins': twitter_plugins,
                                                      'acc_id': t.id}))
            tasks.put((0,{'site': 'twitter', 'op': TASK_FETCH_LISTS,
                                               'data': lists[i] if len(lists)>i else [], 'fetch': t.fetch_list_tweets,
                                               'store': store, 'plugins': twitter_plugins, 'acc_id': t.id}))
            tasks.put((0,{'site': 'twitter', 'op': TASK_FETCH_USER,
                                               'data': users[i] if len(users)>i else [], 'fetch': t.fetch_user_timeline,
                                               'store': store, 'plugins': twitter_plugins, 'acc_id': t.id}))
        # for i in range(TWITTER_CYCLES_PER_HOUR):
        #     t = self._twitter[i % len(self._twitter)]
        #     tasks = self.__put_to_queue__(tasks, {'site': 'twitter', 'op': TASK_EXPLORE,
        #                                           'data': {'remaining': remaining_users,
        #                                                    'bulk_lists': bulk_lists,
        #                                                    'total_followed': users,
        #                                                    'user_lists': lists,
        #                                           },
        #                                           'fetch': t.explore,
        #                                           'store': st.save_candidates,
        #                                           'plugins': twitter_plugins,
        #                                           'acc_id': t.id})
        #     tasks = self.__put_to_queue__(tasks,
        #                                   {'site': 'twitter', 'op': TASK_UPDATE_WALL,
        #                                    'data': timeline, 'fetch': t.fetch_home_timeline,
        #                                    'store': store, 'plugins': twitter_plugins,
        #                                    'acc_id': t.id})
        #     if len(bulk_lists) > i:
        #         tasks = self.__put_to_queue__(tasks, {'site': 'twitter', 'op': TASK_BULK_RETRIEVE,
        #                                               'data': bulk_lists[i],
        #                                               'fetch': t.fetch_bulk_tweets, 'store': store,
        #                                               'plugins': twitter_plugins,
        #                                               'acc_id': t.id})
        #     if len(lists) > i:
        #         tasks = self.__put_to_queue__(tasks,
        #                                       {'site': 'twitter', 'op': TASK_FETCH_LISTS,
        #                                        'data': lists[i], 'fetch': t.fetch_list_tweets,
        #                                        'store': store, 'plugins': twitter_plugins, 'acc_id': t.id})
        #     if len(users) > i:
        #         tasks = self.__put_to_queue__(tasks,
        #                                       {'site': 'twitter', 'op': TASK_FETCH_USER,
        #                                        'data': users[i], 'fetch': t.fetch_user_timeline,
        #                                        'store': store, 'plugins': twitter_plugins, 'acc_id': t.id})
        return tasks

    def __prepare_work__(self):
        tasks = Queue.PriorityQueue()
        for s in self._sites:
            if s == 'twitter':
                self.__prepare_twitter__(tasks)
        return tasks

    def __put_to_queue__(self, q, i):
        'Insert task i into queue q in an equally spaced manner'
        if q.queue and i['op'] == q.queue[-1]['op']:
            if i['op'] != q.queue[0]['op']:
                top = q.queue[0]
                bottom = q.queue[-1]
                q.queue[0] = bottom
                q.queue[-1] = top
                q.put(i)
            elif len(q.queue) % 2 == 0:
                m = len(q.queue) / 2
                mid = q.queue[m]
                q.queue[m] = i
                last = q.queue[-1]
                q.queue[-1] = mid
                q.put(last)
            else:
                m = len(q.queue) / 2
                mid = q.queue[m]
                q.queue[m] = i
                q.put(mid)
        else:
            q.put(i)
        return q
    def __update_future_queue__(self,data):
        'Update the queue for the hybrid model'
        if not data:
            return
        users=data[1]
        topics=data[0]
        self._target_queue['users'] = [(users[k],k) for k in users.keys()]
        self._trends = [(topics[k],k)for k in topics.keys()] if topics else []
        #heapify(self._target_queue)
        #heapify(self._trends)

    def __get_top_n_accounts__(self,n):
        return nlargest(n,self._target_queue["users"])

    def __get_top_n_trends__(self,n):
        return nlargest(n,self._trends)

    def __get_data__(self,task):
        if self._use==TWITTER_HYBRID_MODEL and self._target_queue['users'] and task in [TASK_FETCH_USER,TASK_BULK_RETRIEVE]:
            if task == TASK_BULK_RETRIEVE:
                predicted = [self.__get_top_n_accounts__(TWITTER_BULK_LIST_SIZE) for i in range(int(TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE*PARTITION_FACTOR))]
                normal = self._target_queue[task].get()
                self._target_queue[task].put(normal)
                return predicted + random.sample(normal,TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE-len(predicted))
            elif task == TASK_FETCH_USER:
                return self.__get_top_n_accounts__(TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS)
        else:
            return self._target_queue[task].get()

    def __put_data__(self,task,data):
        self._target_queue[task].put(data)

    def request_work(self, task):
        'Request a new task once the old one is finished'
        print 'before ' + str([v['op'] for v in self._tasks.queue])
        if task['site'] != 'sleep':
            # self._tasks = self.__put_to_queue__(self._tasks,task)
            self._tasks.put((task['timeout'],task))
            with self._lock:
                self._cycles[task['op']] += 1
            self.__put_data__(task['op'],task['data'])
            #    self._timeouts[task['acc_id']][task['op']] = task['timeout']
            print 'after' + str([v['op'] for v in self._tasks.queue])
        if not self._tasks.queue:
            return {'site': 'sleep', 'time': 5}
        top = self._tasks.queue[0]
        # if self._timeouts[task['acc_id']][top['op']] > dt.datetime.now():
        #     timeout = self._timeouts[task['acc_id']][top['op']]
        #     wait = (timeout - dt.datetime.now()).total_seconds()
        #     return dict(site='sleep', time=wait)
        now = time.time()
        if top[0]>now:
            wait = top[0]-now
            return dict(site='sleep',time=wait)
        t = self._tasks.get()
        t['data']= self.__get_data__(t['op'])
        # WARNING CHANGE THIS VALUE ON 19 January 2038 FOR 32 bit CPUs OR AT 15:30:08 ON 4 December 292,277,026,596 FOR 64 bit CPUs
        with self._lock:
            self._timeouts[t['acc_id']][t['op']] = dt.datetime(1970, 1, 1)
        self._tasks.task_done()
        return t
