__author__ = 'tony petrov'

import threading
import minion
import handlers
import datetime as dt
#task={}
# 'site':'twitter,instagram,blah blah'          - site from which data will be retrieved
# 'op':1,2,3,...                                - code of the operation performed refers to the fetch function that the crawler is executing in this task
# 'data':[2032,321,23213,123]                   - contains ids/names/lists of users the minion should get data for
# 'fetch':Handler.f                             - data fetching function from a social media handler
# 'store':f(x)                                  - address of function to which the data should be returned
# 'timeout':213123                              - tells the scheduler that the task is unavailable for execution until the timestamp==time.now()
class Scheduler:
    def __init__(self,**kwargs):
        self._thread_num=1
        self._minions=[]
        self._sites=kwargs['sites'] if 'sites' in kwargs.keys() else ['twitter']
        self._store=kwargs['store'] if 'store' in kwargs.keys() else lambda x:x
        self._tasks=self.__prepare_work__()

    def start(self):
        lock=threading.Lock()
        for i in range(self._thread_num):
            task=self._tasks.pop()
            m=minion.Minion(task,self,lock)
            self._minions.append(m)
            self._tasks.append(task)
            m.start()
            m.join()
        return
    def __prepare_work__(self):
        tasks=[]
        for s in self._sites:
            if s=='twitter':
                t=handlers.TwitterHandler([],[])
                tasks.append({'site':'twitter','op':0,'data':[],'fetch':t.fetch_bulk_tweets,'store':self._store})
                tasks.append({'site':'twitter','op':1,'data':[],'fetch':t.fetch_list_tweets,'store':self._store})
                tasks.append({'site':'twitter','op':2,'data':[],'fetch':t.fetch_user_timeline,'store':self._store})
                tasks.append({'site':'twitter','op':3,'data':[],'fetch':t.fetch_home_timeline,'store':self._store})
        return tasks

    def request_work(self,task):
        if task['site']!='sleep':
            self._tasks.append(task)
        if('timeout' in self._tasks[0].keys() and self._tasks[0]["timeout"]<dt.datetime.now()):
            wait =(self._tasks[0]["timeout"] - dt.datetime.now()).total_seconds()
            return {'site':'sleep','time':wait}
        t=self._tasks.pop()
        return t
