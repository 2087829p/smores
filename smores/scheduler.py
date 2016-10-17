__author__ = 'tony petrov'

import threading
import datetime as dt

from smores import storage as st, minion, handlers



#task={}
# 'site':'twitter,instagram,blah blah'          - site from which data will be retrieved
# 'op':1,2,3,...                                - code of the operation performed refers to the fetch function that the crawler is executing in this task
# 'data':[2032,321,23213,123]                   - contains ids/names/lists of users the minion should get data for
# 'fetch':Handler.f                             - data fetching function from a social media handler
# 'store':f(x)                                  - address of function to which the data should be returned
# 'timeout':213123                              - tells the scheduler that the task is unavailable for execution until the timestamp==time.now()
TASK_EXPLORE=0
TASK_BULK_RETRIEVE=1
TASK_FETCH_LISTS=2
TASK_FETCH_USER=3
TASK_UPDATE_WALL=4

class Scheduler:
    def __init__(self,**kwargs):
        self._thread_num=1
        self._minions=[]
        self._sites=kwargs['sites'] if 'sites' in kwargs.keys() else ['twitter']
        self._store=kwargs['store'] if 'store' in kwargs.keys() else lambda x:x
        if('use' in kwargs):
            if kwargs['use']=='stream':
                pass
            elif kwargs['use']=='both':
                pass
            else:
                pass
        self._tasks=self.__prepare_work__()

    def start(self):
        lock=threading.Lock()
        for i in range(self._thread_num):
            task=self._tasks.pop()
            m= minion.Minion(task,self,lock)
            self._minions.append(m)
            self._tasks.append(task)
            m.start()
            m.join()
        return
    def __prepare_work__(self):
        tasks=[]
        for s in self._sites:
            if s=='twitter':
                t= handlers.TwitterHandler([],[])
                tasks.append({'site':'twitter','op':TASK_EXPLORE,'data':st.load_data('\\data\\twitter\\remaining'),'fetch':t.explore,'store':None})
                tasks.append({'site':'twitter','op':TASK_BULK_RETRIEVE,'data':st.load_data('\\data\\twitter\\bulk_lists'),'fetch':t.fetch_bulk_tweets,'store':self._store})
                tasks.append({'site':'twitter','op':TASK_FETCH_LISTS,'data':st.load_data('\\data\\twitter\\lists'),'fetch':t.fetch_list_tweets,'store':self._store})
                tasks.append({'site':'twitter','op':TASK_FETCH_USER,'data':st.load_data('\\data\\twitter\\users'),'fetch':t.fetch_user_timeline,'store':self._store})
                tasks.append({'site':'twitter','op':TASK_UPDATE_WALL,'data':st.load_data('\\data\\twitter\\home'),'fetch':t.fetch_home_timeline,'store':self._store})
        return tasks

    def __load_bucket_lists_(self):

        return
    def __load__silent_followees(self):
        return
    def __load_lists__(self):
        return

    def request_work(self,task):
        if task['site']!='sleep':
            self._tasks.append(task)
        if('timeout' in self._tasks[0].keys() and self._tasks[0]["timeout"]<dt.datetime.now()):
            wait =(self._tasks[0]["timeout"] - dt.datetime.now()).total_seconds()
            return {'site':'sleep','time':wait}
        t=self._tasks.pop()
        return t
