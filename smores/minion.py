__author__ = 'tony petrov'

import threading
from handlers import TwitterStreamer, TwitterHandler
import time
from constants import *
import datetime
import copy



class Minion(threading.Thread):
    def __init__(self, task, lock, scheduler):
        threading.Thread.__init__(self)
        self._task = task
        self._is_running = True
        self._scheduler = scheduler
        self._lock = lock
        self._cond = threading.Condition()

    def interrupt(self):
        self._is_running = False
        with self._cond:
            self._cond.notifyAll()

    def __request_work__(self, work_set):
        # self._task['site'] = 'sleep'
        self._task['timeout'] = time.time() + (RUNNING_CYCLE if self._task['site'] == 'twitter'
                                               else DEFAULT_SOCIAL_MEDIA_CYCLE)  # datetime.datetime.now() + datetime.timedelta(minutes = TWITTER_CYCLE_DURATION)
        while (not work_set):
            # with self._lock:
            self._task = self._scheduler.request_work(self._task)
            if self._task['site'] == 'sleep':
                wakeup = self._task['time'] + time.time()
                print "%s sleeping for %f seconds waking up at %s" % (
                self.name, self._task['time'], datetime.datetime.fromtimestamp(wakeup).strftime('%Y-%m-%d %H:%M:%S'))
                with self._cond:
                    self._cond.wait(self._task['time'])
            else:
                work_set = self._task['data']
            if not self._is_running:
                break
        return work_set

    def run(self):
        work_set = copy.deepcopy(self._task['data'])
        fetch = self._task['fetch']
        data = []
        # print 'executing ' + str(self._task['op'])
        while self._is_running:
            if not work_set:
                work_set = self.__request_work__(work_set)
                fetch = self._task['fetch']
            try:
                if isinstance(work_set, list):
                    data = fetch(work_set.pop())
                    print self.name + ' executing ' + str(self._task['op']) + ' ' + str(len(work_set)) + ' items left'
                else:
                    print self.name + ' executing ' + str(self._task['op'])
                    data = fetch(work_set)
                    work_set = []
            except Exception as e:
                print "Thread" + str(self.name) + " encountered error " + e.message + " task num = " + str(
                    self._task['op'])
                work_set = self.__request_work__([])
                print 'executing ' + str(self._task['op'])
                fetch = self._task['fetch']
            if self._task['plugins'] and self._task['op'] != TASK_EXPLORE:
                for p in self._task['plugins']:
                    p.data_available(data)
            time.sleep(POLITENESS_VALUE)
            # with self._lock:
            self._task['store'](data)


class Streamion(Minion):
    def __init__(self, stream_creds, task, lock, scheduler):
        super(Streamion, self).__init__(task, lock, scheduler)
        self._creds = stream_creds if not isinstance(stream_creds, list) else stream_creds[0]

    def interrupt(self):
        super(Streamion, self).interrupt()
        self._streamer.disconnect()

    def data_available(self,data):
        if self._task['plugins']:
            for p in self._task['plugins']:
                p.data_available(data)
        self._task['store'](data)

    def run(self):
        print "Starting streamer"
        import constants as c
        from test_struct import Mock_Twitter_Stream
        self._streamer = TwitterStreamer(self._creds['app_key'], self._creds['app_secret']
                                         , self._creds['oauth_token'], self._creds['oauth_token_secret']) if not c.TESTING else Mock_Twitter_Stream(self._creds)
        self._twitter = TwitterHandler(self._creds, id=self._creds['id'])
        self._streamer.set_callback(self.data_available)
        # if an error occurs e.g. no internet or twitter is inaccessible terminate thread
        self._streamer.set_error_handler(self.interrupt)
        # a handy functional expression to check if the trends data is data or list of locations for which we want trends
        contains_locations = lambda x: isinstance(x, list) and any([('location' in i or 'woeid' in i) for i in x])
        trends = self._task['data'] if contains_locations(self._task['data']) \
            else self._twitter.get_trends(self._task['data'])
        follow = []
        while (self._is_running):
            "Collecting stream data"
            try:
                if follow:
                    self._streamer.statuses.filter(track=', '.join(trends[:MAX_TACKABLE_TOPICS]), follow=','.join(follow))
                else:
                    self._streamer.statuses.filter(track=', '.join(trends[:MAX_TACKABLE_TOPICS]))
                with self._cond:
                    self._cond.wait(RUNNING_CYCLE)
                trends = self._scheduler.__get_top_n_trends__(MAX_TACKABLE_TOPICS)
                follow = self._scheduler.__get_top_n_accounts__(MAX_FOLLOWABLE_USERS)
                if not trends:
                    print "Requesting trends"
                    trends = self._twitter.get_trends(self._task['data'])
            except Exception as e:
                print "Streamion encountered and error: %s" % e.message
        self._streamer.disconnect()
