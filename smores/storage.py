__author__ = 'tony petrov'

import os
import pickle
import time
import threading
import constants
from concurrent import futures
import Queue


def __abs_path__(fl):
    curr_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    abs_file_path = os.path.join(curr_dir, fl)
    return abs_file_path


def load_data(f):
    data = []
    file_path = __abs_path__(f)
    if not os.path.exists(file_path):
        open(file_path, 'w+').close()
        return data
    with open(file_path, 'rb') as handle:
        try:
            data = pickle.load(handle)
        except Exception as e:
            print "error while opening file " + f + ' cause: ' + e.message
    return data


def save_data(data, fl, append=False):
    if constants.TESTING:
        return
    file_path = __abs_path__(fl)
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except:
            print "could not create missing directory"
            return
    if append:
        data += load_data(fl)
    with open(file_path, 'wb') as handle:
        try:
            pickle.dump(data, handle)
        except Exception as e:
            print "could not save data to file %s cause: %s" % (fl,e.message)
def load_explorer_data():
    import constants as c
    bulk_lists=load_data(c.TWITTER_BULK_LIST_STORAGE)
    lists = load_data(c.TWITTER_LIST_STORAGE)
    users = load_data(c.TWITTER_USER_STORAGE)
    remaining = load_data(c.TWITTER_CANDIDATES_STORAGE)
    data={'remaining':remaining if remaining else[],
          'bulk_lists': bulk_lists if bulk_lists else [],
          'total_followed': users if users else [],
          'user_lists': lists if lists else []}
    return data

class Format_Error(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def read_login(f):
    data = []
    file_path = __abs_path__(f)
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
        return data
    with open(file_path, 'r') as handle:
        content = handle.readlines()
        for l in content:
            data_entry = {}
            l = l.strip('\n')
            l = l.strip("[]")
            entry = l.split(',')
            for e in entry:
                d = e.split(":")
                if (len(d) != 2):
                    raise Format_Error("Unable to parse credentials file due to error in formatting")
                data_entry[d[0]] = d[1]
            data.append(data_entry)
    return data


def save_candidates(candidates):
    save_data(candidates,constants.TWITTER_CANDIDATES_STORAGE)


# 1 db per day
# 1 collection per hour
# as many tweets as possible aka documents
# if time == available then https://www.sitepoint.com/caching-a-mongodb-database-with-redis/
class StorageSystem:
    def __init__(self, ip, port, thread_count):
        self.ip = ip
        self.port = port
        self._current_db = time.strftime("%x")  # sets the name of the current db to the current date
        self._current_collection = time.strftime(
            "%X")  # set the current collection to the current time aka current hour
        self._pool = futures.ThreadPoolExecutor(max_workers=thread_count)

    # NEVER TO BE CALLED BY ANYONE BUT SCHEDULER
    def switch_db_context(self):
        self._current_db = time.strftime("%x")

    # TO BE USED ONLY FOR TESTING
    def set_db_context(self, c):
        self._current_db = c

    # NOT TO BE CALLED BY USER MUST BE CALLED ONLY BY SCHEDULER
    def switch_collection_context(self):
        self._current_collection = time.strftime("%X")

    def __perform_write__(self, data, ip, port, **kwargs):
        'Write the new data to the specified server'
        import pymongo
        try:
            mongo = pymongo.MongoClient(ip, port)
            db = mongo[kwargs['current_db']]
            db[kwargs['current_collection']].insert_many(data, False)
            mongo.close()
        except:
            raise ValueError('MongoDB server ' + ip + ':' + str(port)
                             + ' endpoint data is incorrect or server is down')

    def write(self, data):
        'Enqueue data that the storage system will attempt to save'
        self._pool.submit(self.__perform_write__,
                          data, self.ip,
                          self.port,
                          current_db=self._current_db,
                          current_collection=self._current_collection)

    def shutdown(self):
        print "Storage system is shutting down please wait for all pending IO tasks to complete"
        self._pool.shutdown(True)


# http://www.bogotobogo.com/python/Multithread/python_multithreading_Synchronization_Condition_Objects_Producer_Consumer.php
class Filter(threading.Thread):
    # service used to specify which task should results should be fed to filter refer to service plugins in constants.py
    def __init__(self, service, store, filters):
        threading.Thread.__init__(self)
        self._for = service
        self._data = Queue.Queue()
        self._store = store
        self._plugins = filters
        self._cond = threading.Condition()
        self._lock = threading.Lock()
        self.daemon = True
        self._running = True
        # self.start()

    def set_store(self, store):
        self._store = store

    def data_available(self, data):
        'Notify the plugin that new data is available for processing'
        self._data.put(data)
        with self._lock:
            with self._cond:
                self._cond.notify()

    def start(self):
        threading.Thread.start(self)
        if not self._plugins:
            return
        for p in self._plugins:
            p.start()

    def interrupt(self):
        'Terminate plugin and its pipeline'
        with self._lock:
            self._running = False
            with self._cond:
                self._cond.notify()
        if self._plugins:
            for p in self._plugins:
                p.interrupt()

    def register_plugin(self, p):
        'Add new plugin to the end of the pipeline'
        if isinstance(p, Filter):
            self._plugins.append(p)

    def run(self):
        while self._running:
            while self._data:
                data = self.process(self._data.get())
                self._data.task_done()
                if self._store:
                    self._store(data)
                if self._plugins:
                    for p in self._plugins:
                        p.data_available(data)
            self._cond.wait()

    def process(self, data):
        'Processes the input data must be overridden and implemented in every class that subclasses this one'
        raise NotImplementedError()
