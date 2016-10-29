__author__ = 'tony petrov'
import scheduler as s
import constants as c
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

def model_comparison():
    pass

politeness_test()
#crawl(use='model')