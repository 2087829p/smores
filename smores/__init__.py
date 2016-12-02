__author__ = 'tony petrov'
import scheduler as s
import constants as c
import sys
scheduler=None

def crawl(**kwargs):
    global scheduler
    use = kwargs['use'] if 'use' in kwargs.keys() else 'both'
    ip = kwargs['ip'] if 'ip' in kwargs.keys() else 'localhost'
    port = kwargs['port'] if 'port' in kwargs.keys() else 27017
    scheduler=s.Scheduler(use=use,site='twitter',ip=ip,port=port)
    scheduler.start()
    command = ''
    print 'Crawler started to stop it type q'
    while command != 'q':
        command=raw_input()
    scheduler.terminate()
def stop():
    global  scheduler
    scheduler.terminate()
def politeness_test():
    c.TESTING=True
    sh=s.Scheduler(use='model',site='twitter')
    sh.start()
    import time
    time.sleep(60)
    sh.terminate()
    if sh._twitter._twitter.passed():
        print 'Politeness tests are passed'
    else:
        print 'Tests failed:'
        print sh._twitter._twitter.get_failures()
    sys.exit(0)
def printStats(**kwargs):
    total = 0
    unique = 0
    users = 0
    cycles = 0
    data = []
    pipeline = [
        {'$unwind':'$user'},
        {'$group':{
            '_id':'$id',
            'unique_tweets':{'$addToSet':'$id'},
            'unique_users':{'$addToSet':'$user.id'},
            'count':{'$sum':1}
            }
        },
        {'$project':{
            '_id':0,
            'total_tweets':'$count',
            'unique_tweets':{'$size':'unique_tweets'},
            'users':{'$size':'unique_users'}
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
                cycles+=1
            mongo.close()
    except:
            raise ValueError('MongoDB server ' + kwargs['ip'] + ':' + str(kwargs['port'])
                             + ' endpoint data is incorrect or server is down')
    print "\n results from "+kwargs['model'] + \
          "\n total tweets gathered = " + str(total) + \
          "\n tweets per cycle = " + str(total/cycles) +\
          "\n total unique tweets = " + str(unique) +\
          "\n total users crawled = " + str(users) + \
          "\n users per cycle = " + str(users/cycles)

def model_comparison():
    import storage,time
    mdb="mdb"+time.strftime("%x")
    db1 = storage.StorageSystem('localhost',0,10)
    db1.set_db_context(mdb)
    strm="strm"+time.strftime("%x")
    db2 = storage.StorageSystem('localhost',0,4)
    db2.set_db_context(strm)
    sh=s.Scheduler(use='both',site='twitter',storage={'model':db1,'stream':db2})
    sh.start()
    import time
    time.sleep(900)
    sh.terminate()
    db1.shutdown()
    db2.shutdown()
    from concurrent import futures
    with futures.ThreadPoolExecutor(max_workers=2) as pool:
        pool.submit(printStats,ip='localhost',port='',db=mdb,model='model')
        pool.submit(printStats,ip='localhost',port='',db=mdb,model='streaming')
    sys.exit(0)
import numpy as np
from utils import *
n=NeuralNetwork(6,1)
n.add_hidden_layer(10)
n.train(np.array([1,1,1,1,1,1]),np.array([1]),5)
n.train(np.array([1,1,1,1,1,1]),np.array([1]))
n.train(np.array([0,0,0,0,0,0]),np.array([0]),5)
print n.predict(np.array([0]*6))
politeness_test()
#crawl(use='model')