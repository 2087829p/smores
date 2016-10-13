__author__ = 'tony petrov'
import threading
import time

class Minion(threading.Thread):
    def __init__(self, task,scheduler,lock):
        threading.Thread.__init__(self)
        self._task = task
        self._is_running = True
        self._scheduler=scheduler
        self._lock=lock

    def interrupt(self):
        self._is_running=False

    def __request_work__(self):
        while(not self._task['data']):
            self._lock.acquire()
            self._task=self._scheduler.request_work(self._task)
            self._lock.release()
            if(self._task['site']=='sleep'):
                time.sleep(self._task['time'])


    def run(self):
        work_set=self._task['data']
        while(self._is_running):
            if not work_set:
                self.__request_work__()
                work_set=self._task['data']
            data=self._task['fetch'](work_set.pop())
            self._lock.acquire()
            self._task['store'](data)
            self._lock.release()



