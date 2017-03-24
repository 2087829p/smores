__author__ = 'tony petrov'

import threading
from handlers import TwitterStreamer
import copy
import time
from constants import *
import datetime
import copy
from twython import TwythonRateLimitError,TwythonError



class Minion(threading.Thread):
    def __init__(self, task, lock, scheduler):
        threading.Thread.__init__(self)
        self._task = task
        self._is_running = True
        self._scheduler = scheduler
        self._lock = lock
        self._cond = threading.Condition()
        self.daemon = True

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
                    print self.name + ' executing ' + str(self._task['op']) + ' ' + str(len(work_set)) + ' items left'
                    data = fetch(work_set.pop())
                else:
                    print self.name + ' executing ' + str(self._task['op'])
                    data = fetch(work_set)
                    work_set = []
            except TwythonRateLimitError as le:
                # we're told to back off so we back off
                work_set = self.__request_work__([])
                print 'executing ' + str(self._task['op'])
                fetch = self._task['fetch']
            except TwythonError as te:
                # twitter is telling us that there's a problem with the query
                if not te.error_code in [401,404]:
                    # if its not a missing item or unauthorized access then we should back off
                    work_set = self.__request_work__([])
                    print 'executing ' + str(self._task['op'])
                    fetch = self._task['fetch']
            except Exception as e:
                # something else happened just tell the user
                print "Thread" + str(self.name) + " encountered error " + e.message + " task num = " + str(
                    self._task['op'])
            if self._task['plugins'] and self._task['op'] != TASK_EXPLORE:
                for p in self._task['plugins']:
                    p.data_available(copy.deepcopy(data)) #since we might have alot of plugins give them a copy
                                                          #prevents the filters from destroying each others data
            time.sleep(POLITENESS_VALUE)
            # with self._lock:
            if self._task['store']:
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
                p.data_available(copy.deepcopy(data))
        if self._task['store']:
            self._task['store'](data)

    def run(self):
        import constants as c
        print "Starting streamer"
        from test_struct import Mock_Twitter_Stream
        self._streamer = TwitterStreamer(self._creds['app_key'], self._creds['app_secret']
                                         , self._creds['oauth_token'], self._creds['oauth_token_secret']) \
            if not c.TESTING else Mock_Twitter_Stream(self._creds)
        self._streamer.set_callback(self.data_available)
        # if an error occurs e.g. no internet or twitter is inaccessible terminate thread
        self._streamer.set_error_handler(self.interrupt)
        trends = self._task['data']
        follow = []
        while self._is_running:
            "Collecting stream data"
            try:
                if not c.FILTER_STREAM:
                    self._streamer.statuses.sample()
                else:
                    if follow:
                        self._streamer.statuses.filter(track=','.join(trends[:MAX_TRACKABLE_TOPICS]), follow=','.join(follow))
                    else:
                        self._streamer.statuses.filter(track=','.join(trends[:MAX_TRACKABLE_TOPICS]))
                    with self._cond:
                        self._cond.wait(RUNNING_CYCLE)
                    trends = self._scheduler.__get_top_n_trends__(MAX_TRACKABLE_TOPICS)
                    follow = self._scheduler.__get_top_n_accounts__(MAX_FOLLOWABLE_USERS)
            except Exception as e:
                print "Streamion encountered an error: %s" % e.message
        self._streamer.disconnect()
