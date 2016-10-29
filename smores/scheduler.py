__author__ = 'tony petrov'

import threading
import datetime as dt

from smores import storage as st
import minion as m
import handlers
import constants as const
import utils
import Queue

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
DB_CONTEXT_SWITCH_TIMEOUT = 86400  # every day new db
COLLECTION_CONTEXT_SWITCH_TIMEOUT = 3600  # every hour aka cycle new collection of docs


class Scheduler:
    def __init__(self, **kwargs):
        self._thread_num = 1
        self._minions = []
        self._sites = kwargs['sites'] if 'sites' in kwargs.keys() else ['twitter']
        self._plugins = kwargs['plugins'] if 'plugins' in kwargs.keys() else []
        self._lock = threading.Lock()
        self._trends = kwargs['trends'] if 'trends' in kwargs.keys() else []
        # WARNING CHANGE THIS VALUE ON 19 January 2038 FOR 32 bit CPUs OR AT 15:30:08 ON 4 December 292,277,026,596 FOR 64 bit CPUs
        self._timeouts=[dt.datetime(1970,1,1) for i in range(TOTAL_TASKS)]
        if const.TESTING:
            pass
            self._store = lambda x: x
        else:
            if 'ip' not in kwargs.keys() and 'port' not in kwargs.keys():
                raise ValueError('IP and port of the MongoDB server must be specified')
            self._storage = st.StorageSystem(kwargs['ip'], kwargs['port'], self._thread_num)
            self._store = self._storage.write
        self._use = kwargs['use'] if 'use' in kwargs else 'minions'

        # self.start()

    def add_filters(self, filters):
        self._plugins += filters

    def start(self):
        if not const.TESTING:
            self._timer1 = threading.Timer(DB_CONTEXT_SWITCH_TIMEOUT, self._storage.switch_db_context)
            self._timer2 = threading.Timer(COLLECTION_CONTEXT_SWITCH_TIMEOUT, self._storage.switch_collection_context)
        if self._use == 'stream':
            self.__setup_streamer__(self._trends)
        elif self._use == 'both':
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
        if not const.TESTING:
            self._timer1.start()
            self._timer2.start()

    def terminate(self):
        # ======replace this with a custom timer class if possible===
        # ref:http://stackoverflow.com/questions/9812344/cancellable-threading-timer-in-python

        # ===========================================================
        for mn in self._minions:
            mn.interrupt()
        for p in self._plugins:
            p.interrupt()
        if not const.TESTING:
            self._timer1.cancel()
            self._timer2.cancel()
            self._storage.shutdown()


    def __setup_minions__(self):
        self._tasks = self.__prepare_work__()
        print [v['op'] for v in self._tasks.queue]
        unique_ops=len(set([t['op'] for t in self._tasks.queue]))
        self._thread_num=min(self._thread_num,unique_ops)
        for i in range(self._thread_num):
            task = self._tasks.get_nowait()
            self._tasks.task_done()
            self._timeouts[task['op']] = dt.datetime.now() + dt.timedelta(minutes = const.TWITTER_CYCLE_DURATION)
            self._minions.append(m.Minion(task, lock=self._lock, scheduler=self))
            #self._tasks.put_nowait(task)

    def __setup_streamer__(self, trend_data):
        login = st.read_login(const.TWITTER_CREDENTIALS)
        serv = const.TWITTER_PLUGIN_SERVICE if self._use == 'both' else const.TWITTER_STREAMING_PLUGIN_SERVICE
        plugins = [p for p in self._plugins if p == serv]
        t = {'site': 'twitter', 'op': TASK_FETCH_STREAM, 'data': trend_data, 'fetch': None, 'store': self._store,
             'plugins': plugins}
        self._minions.append(m.Streamion(login, t, lock=self._lock, scheduler=self))


    def __prepare_twitter__(self, tasks):
        login = st.read_login(const.TWITTER_CREDENTIALS)
        t = handlers.TwitterHandler(login, False)
        self._twitter = t
        serv = const.TWITTER_PLUGIN_SERVICE if self._use == 'both' else const.TWITTER_MODEL_PLUGIN_SERVICE
        twitter_plugins = [p for p in self._plugins if p._for == serv]
        remaining_users = st.load_data(const.TWITTER_CANDIDATES_STORAGE)
        remaining_users = remaining_users if remaining_users else [0]
        bulk_lists = st.load_data(const.TWITTER_BULK_LIST_STORAGE)
        lists = st.load_data(const.TWITTER_LIST_STORAGE)
        users = st.load_data(const.TWITTER_USER_STORAGE)
        timeline = st.load_data(const.TWITTER_WALL_STORAGE)
        tasks.put_nowait({'site': 'twitter', 'op': TASK_EXPLORE,
                          'data': {'remaining':remaining_users,
                                    'bulk_lists':bulk_lists,
                                    'total_followed':users,
                                    'user_lists':lists,
                                   },
                          'fetch': t.explore,
                          'store': st.save_candidates,
                          'plugins': twitter_plugins})
        return tasks
        blg = utils.split_into(bulk_lists, const.TWITTER_MAX_NUM_OF_BULK_LISTS)
        bulk_lists = [l for l in blg]
        lg = utils.split_into(lists, const.TWITTER_MAX_NUMBER_OF_LISTS)
        lists = [l for l in lg]
        ug = utils.split_into(users, const.TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS)
        users = [l for l in ug]
        if (timeline):
            tasks = self.__put_to_queue__(tasks,
                                          {'site': 'twitter', 'op': TASK_UPDATE_WALL,
                                           'data': timeline, 'fetch': t.fetch_home_timeline,
                                           'store': self._store, 'plugins': twitter_plugins})
        for i in range(const.TWITTER_CYCLES_PER_HOUR):
                if len(bulk_lists) > i:
                    tasks = self.__put_to_queue__(tasks, {'site': 'twitter', 'op': TASK_BULK_RETRIEVE,
                                                          'data': bulk_lists[i],
                                                          'fetch': t.fetch_bulk_tweets, 'store': self._store,
                                                          'plugins': twitter_plugins})
                if len(lists) > i:
                    tasks = self.__put_to_queue__(tasks,
                                                  {'site': 'twitter', 'op': TASK_FETCH_LISTS,
                                                   'data': lists[i], 'fetch': t.fetch_list_tweets,
                                                   'store': self._store, 'plugins': twitter_plugins})
                if len(users) > i:
                    tasks = self.__put_to_queue__(tasks,
                                                  {'site': 'twitter', 'op': TASK_FETCH_USER,
                                                   'data': users[i], 'fetch': t.fetch_user_timeline,
                                                   'store': self._store, 'plugins': twitter_plugins})
        return tasks

    def __prepare_work__(self):
        tasks = Queue.Queue()
        for s in self._sites:
            if s == 'twitter':
                tasks = self.__prepare_twitter__(tasks)
        return tasks

    def __put_to_queue__(self, q, i):
        if i['op'] == q.queue[-1]['op']:
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

    def request_work(self, task):
        print 'before ' + str([v['op'] for v in self._tasks.queue])
        if task['site'] != 'sleep':
            #self._tasks = self.__put_to_queue__(self._tasks,task)
            self._tasks.put(task)
            with self._lock:
                self._cycles[task['op']] += 1
                self._timeouts[task['op']]=task['timeout']
            print 'after' + str([v['op'] for v in self._tasks.queue])
        if not self._tasks.queue:
            return {'site':'sleep','time':5}
        top = self._tasks.queue[0]
        if self._timeouts[top['op']] > dt.datetime.now():
                wait = (self._timeouts[top['op']] - dt.datetime.now()).total_seconds()
                return {'site': 'sleep', 'time': wait}
        t = self._tasks.get()
        # WARNING CHANGE THIS VALUE ON 19 January 2038 FOR 32 bit CPUs OR AT 15:30:08 ON 4 December 292,277,026,596 FOR 64 bit CPUs
        with self._lock:
            self._timeouts[t['op']] = dt.datetime(1970,1,1)
        self._tasks.task_done()
        return t
