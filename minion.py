__author__ = 'tony petrov'

import threading
from handlers import TwitterStreamer, TwitterHandler
import time
from constants import *
import datetime


class Minion(threading.Thread):
    def __init__(self, task, lock,scheduler):
        threading.Thread.__init__(self)
        self._task = task
        self._is_running = True
        self._scheduler = scheduler
        self._lock=lock
        self._cond = threading.Condition()

    def interrupt(self):
        self._is_running = False
        with self._cond:
             self._cond.notifyAll()

    def __request_work__(self,work_set):
        #self._task['site'] = 'sleep'
        self._task['timeout'] = time.time()+RUNNING_CYCLE#datetime.datetime.now() + datetime.timedelta(minutes = TWITTER_CYCLE_DURATION)
        while (not work_set):
            #with self._lock:
            self._task = self._scheduler.request_work(self._task)
            if self._task['site'] == 'sleep':
                with self._cond:
                    self._cond.wait(self._task['time'])
            else:
                work_set=self._task['data']
            if not self._is_running:
                break
        return work_set


    def run(self):
        work_set = self._task['data']
        fetch=self._task['fetch']
        data = []
        print 'executing ' + str(self._task['op'])
        while self._is_running:
            if not work_set:
                work_set = self.__request_work__(work_set)
                print 'executing ' + str(self._task['op'])
                fetch = self._task['fetch']
            try:
                if isinstance(work_set,list):
                    data = fetch(work_set.pop())
                else:
                    data = fetch(work_set)
                    work_set=[]
            except Exception as e:
                print e.message
                work_set = self.__request_work__([])
                print 'executing ' + str(self._task['op'])
                fetch=self._task['fetch']
            if self._task['plugins']:
                for p in self._task['plugins']:
                    p.data_available(data)
            time.sleep(POLITENESS_VALUE)
            # with self._lock:
            self._task['store'](data)


class Streamion(Minion):
    def __init__(self, stream_creds, task,lock, scheduler):
        super(Streamion, self).__init__(task,lock, scheduler)
        self._creds = stream_creds

    def interrupt(self):
        super(Streamion, self).interrupt()
        self._streamer.disconnect()

    def run(self):
        self._streamer = TwitterStreamer(self._creds['api_key'], self._creds['api_secret']
                                         , self._creds['oath_token'], self._creds['token_secret'])
        self._twitter = TwitterHandler(self._creds)
        self._streamer.set_callback(self._task['store'])
        # if an error occurs e.g. no internet or twitter is inaccessible terminate thread
        # HAS NEVER BEEN TESTED WORKS IN THEORY BUT MIGHT BE BUGGY
        self._streamer.set_error_handler(self.interrupt())
        trends = self._twitter.get_trends(self._task['data'])
        follow = []
        while (self._is_running):
            if follow:
                self._streamer.statuses.filter(track=','.join(trends[:MAX_TACKABLE_TOPICS]),follow = ','.join(follow))
            else:
                self._streamer.statuses.filter(track=','.join(trends[:MAX_TACKABLE_TOPICS]))
            with self._cond:
                self._cond.wait(RUNNING_CYCLE)
            trends=self._scheduler.__get_top_n_trends__(MAX_TACKABLE_TOPICS)
            follow = self._scheduler.__get_top_n_accounts__(MAX_FOLLOWABLE_USERS)
            if not trends:
                trends = self._twitter.get_trends(self._task['data'])
            # self._streamer.disconnect()
