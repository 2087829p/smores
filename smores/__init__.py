__author__ = 'tony petrov'
import scheduler as s
import constants as c
import sys
from storage import Filter
from utils import *
from memory_profiler import profile
import json
import copy
from storage import __abs_path__
scheduler = None


def crawl(**kwargs):
    global scheduler
    use = kwargs['use'] if 'use' in kwargs.keys() else 'both'
    ip = kwargs['ip'] if 'ip' in kwargs.keys() else 'localhost'
    port = kwargs['port'] if 'port' in kwargs.keys() else 27017
    scheduler = s.Scheduler(use=use, site='twitter', ip=ip, port=port)
    scheduler.start()
    command = ''
    print 'Crawler started to stop it type q'
    while command != 'q':
        command = raw_input()
    scheduler.terminate()


def stop():
    global scheduler
    scheduler.terminate()


def politeness_test():
    c.TESTING = True
    sh = s.Scheduler(use='model', site='twitter', multicore=True)
    sh.start()
    import time
    t = 60
    try:
        while t > 0:
            time.sleep(1)
            t -= 1
    except KeyboardInterrupt:
        pass
    sh.terminate()
    if sh._handlers[0]._twitter.passed():
        print 'Politeness tests are passed'
    else:
        print 'Tests failed:'
        print sh._handlers[0]._twitter.get_failures()
    #sys.exit(0)


def printStats(**kwargs):
    total = 0
    unique = 0
    users = 0
    cycles = 0
    data = []
    pipeline = [
        {'$unwind': '$user'},
        {'$group': {
            '_id': '$id',
            'unique_tweets': {'$addToSet': '$id'},
            'unique_users': {'$addToSet': '$user.id'},
            'count': {'$sum': 1}
        }
        },
        {'$project': {
            '_id': 0,
            'total_tweets': '$count',
            'unique_tweets': {'$size': 'unique_tweets'},
            'users': {'$size': 'unique_users'}
        }
        }
    ]
    try:
        import pymongo

        mongo = pymongo.MongoClient(kwargs['ip'], kwargs['port'])
        db = mongo[kwargs['db']]
        cols = db.collection_names()
        for c in cols:
            data = db[c].aggregate(pipeline)
            total += db[c].count()
            unique += db[c].distinct("id").length
            users += db[c].distinct("user.id").length
            cycles += 1
        mongo.close()
    except:
        raise ValueError('MongoDB server ' + kwargs['ip'] + ':' + str(kwargs['port'])
                         + ' endpoint data is incorrect or server is down')
    print "\n results from " + kwargs['model'] + \
          "\n total tweets gathered = " + str(total) + \
          "\n tweets per cycle = " + str(total / cycles) + \
          "\n total unique tweets = " + str(unique) + \
          "\n total users crawled = " + str(users) + \
          "\n users per cycle = " + str(users / cycles)


class StatsFilter(Filter):
    def __init__(self, service, store, filters):
        super(StatsFilter, self).__init__(service, store, filters)
        self.unique_users = set()
        # self.total_users = 0
        self.total_tweets = 0
        self.unique_tweets = 0
        self.lost_data = 0
        self.data_size = 0
        self.foreign = 0
        self.distribution = dict()
    def get_distribution(self):
        from collections import Counter
        with self._lock:
            d = dict(Counter(self.distribution.values()))
        return d
    def get_raw_distribution(self):
        d_copy = None
        with self._lock:
            d_copy=copy.deepcopy(self.distribution)
        return d_copy
    def process(self, data):
        #print "processing data"
        if not isinstance(data, list):
            try:
                self.unique_users.add(data['user']['id'])
                self.unique_tweets += 1 if 'retweeted_status' not in data else 0
                self.total_tweets += 1
                self.data_size += sys.getsizeof(data)
                self.foreign += 1 if not all_ascii(data['text']) else 0
                with self._lock:
                    self.distribution[data['user']['id']] = self.distribution.get(data['user']['id'],0) + 1
                #print "1 tweet processed"
            except Exception as e:
                #print "Error in tweet format: " + str(data)
                self.lost_data += 1
        else:
            success = 0
            #print "data in %d" % len(data)
            for t in data:
                try:
                    self.unique_users.add(t['user']['id'])
                    self.unique_tweets+= 1 if 'retweeted_status' not in t else 0
                    self.total_tweets += 1
                    self.foreign += 1 if not all_ascii(t['text']) else 0
                    self.data_size += sys.getsizeof(t)
                    with self._lock:
                        self.distribution[t['user']['id']] = self.distribution.get(t['user']['id'], 0) + 1
                    success += 1
                except Exception as e:
                    #print "Error in tweet format: " + str(t)
                    self.lost_data += 1
            print "%d tweets processed" % success


def explore_only(testing,t=3600):
    c.EXPLORING = True
    c.TESTING = testing
    sh = s.Scheduler(use='model', site='twitter', storage=lambda x: x, multicore=False)
    sh.start()
    import time
    try:
        while t > 0:
            time.sleep(1)
            t -= 1
    except KeyboardInterrupt:
        pass
    sh.terminate()

@profile
def model_comparison():
    # import storage, time

    # mdb = "mdb" + time.strftime("%x")
    # db1 = storage.StorageSystem('localhost', 0, 10)
    # db1.set_db_context(mdb)
    # strm = "strm" + time.strftime("%x")
    # db2 = storage.StorageSystem('localhost', 0, 4)
    # db2.set_db_context(strm)
    f1 = StatsFilter(TWITTER_STREAMING_PLUGIN_SERVICE, lambda x: x, None)
    f2 = StatsFilter(TWITTER_HARVESTER_PLUGIN_SERVICE, lambda x: x, None)
    #c.TESTING=True
    sh = s.Scheduler(use='both', site='twitter', storage=lambda x: x, plugins=[f1,f2], multicore=True)
    sh.start()
    from time import gmtime, strftime
    print "Test started at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    import time
    t = 3600
    try:
        while t > 0:
            time.sleep(1)
            t -= 1
    except KeyboardInterrupt:
        pass
    sh.terminate()
    # db1.shutdown()
    # db2.shutdown()
    # from concurrent import futures
    print "\nHarvester data"
    print "total tweets = %d\nunique tweets = %d\nunique users = %d\nloses = %d\ndata size = %d MB\nnon-English tweets = %d\n" % (
    f2.total_tweets, f2.unique_tweets, len(f2.unique_users), f2.lost_data,f2.data_size/1000000,f2.foreign)
    print "\npurity = %f\n tweets per user= %f\n" % (
    f2.unique_tweets / float(f2.total_tweets), f2.total_tweets / float(len(f2.unique_users)))
    json.dump(f2.get_raw_distribution(), open(__abs_path__("data\harvester_distribution.json"), 'w'))
    print "Streaming model data"
    print "total tweets = %d\nunique tweets = %d\nunique users = %d\nloses = %d\ndata size = %d MB\nnon-English tweets = %d\n" % (
    f1.total_tweets, f1.unique_tweets, len(f1.unique_users), f1.lost_data, f1.data_size/1000000,f1.foreign)
    print "\npurity = %f\n tweets per user= %f\n" % (
    f1.unique_tweets / float(f1.total_tweets), f1.total_tweets / float(len(f1.unique_users)))
    print "Test completed at "+ strftime("%Y-%m-%d %H:%M:%S", gmtime())
    json.dump(f1.get_raw_distribution(), open(__abs_path__("data\stream_distribution.json"), 'w'))

    # with futures.ThreadPoolExecutor(max_workers=2) as pool:
    #    pool.submit(printStats, ip='localhost', port='', db=mdb, model='model')
    #    pool.submit(printStats, ip='localhost', port='', db=mdb, model='streaming')
    #sys.exit(0)
@profile
def run_hybrid(t=3600,testing=False,classifier=PERCEPTRON_CLASSIFIER):
    f1 = StatsFilter(TWITTER_PLUGIN_SERVICE, lambda x: x, None)
    if testing:
        c.TESTING = True
        c.RANK_RESET_TIME=15
    c.FILTER_STREAM = True
    sh = s.Scheduler(use='hybrid', site='twitter', storage=lambda x: x, plugins=[f1],
                     multicore=True,classifier=classifier)
    sh.start()
    from time import gmtime, strftime
    print "Test started at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    import time
    try:
        while t > 0:
            time.sleep(1)
            t -= 1
    except KeyboardInterrupt:
        pass
    sh.terminate()
    print "Results"
    print "total tweets = %d\nunique tweets = %d\nunique users = %d\nloses = %d\ndata size = %d MB \nnon-English tweets = %d\n" % (
        f1.total_tweets, f1.unique_tweets, len(f1.unique_users), f1.lost_data,f1.data_size/1000000,f1.foreign)
    print "Features"
    print "\npurity = %f\n tweets per user= %f\n" % (f1.unique_tweets/float(f1.total_tweets),f1.total_tweets/float(len(f1.unique_users)))
    print "Test completed at " + strftime("%Y-%m-%d %H:%M:%S", gmtime())
    json.dump(f1.get_raw_distribution(),open(__abs_path__("data\hybrid_distribution.json"),'w'))
    json.dump(f1.get_distribution(),open(__abs_path__("data\processed_hybrid_distribution.json"),'w'))
    #sys.exit(0)
def full_testing():
    """""performs offline testing of the crawler to try and find bugs and issues"""
    #tests to see if the system complies with politeness rules
    politeness_test()
    #=========tests to see if the classifiers and ranking filter can handle broken data=============
    run_hybrid(60,True,PERCEPTRON_CLASSIFIER)
    run_hybrid(60,True,DEEP_NEURAL_NETWORK_CLASSIFIER)
    run_hybrid(60,True,K_MEANS_CLASSIFIER)
    #================================================================================================
    sys.exit(0)
# politeness_test()
#model_comparison()
#explore_only()
run_hybrid(3600,False,DEEP_NEURAL_NETWORK_CLASSIFIER)
#crawl(use='model')
