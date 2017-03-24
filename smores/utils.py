__author__ = 'tony petrov'
import threading
import numpy as np
from constants import *
import math
import time
import constants as c


def split_into(l, n):
    'Splits the list into smaller lists with n elements each'
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def fit_in_range(min, max, x):
    """fits a number(x) within a specified range between min and max"""
    return (x - min) / (max - min)
# coverts twitter timestamp to system time in seconds since Unix epoch
get_tweet_timestamp = lambda t:time.mktime(time.strptime(t["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))
# flattens a multidimensional array into a 1-dimensional array
flatten = lambda l: [i for sl in l for i in sl]
# removes Twitter accounts that are protected or have to few tweets to be deemed active
user_filter = lambda x:filter(lambda y:y['protected']==False and y['statuses_count']>c.MIN_TWITTER_STATUSES_COUNT,x)
# a handy functional expression to check if the trends data is data or list of locations for which we want trends
contains_locations = lambda x: isinstance(x, list) and any(
                        [('location' in i or 'woeid' in i or 'lat' in i or 'long' in i) for i in x])
# determines whether a string contains only ascii characters
all_ascii = lambda x:all(ord(c) < 128 for c in x)
class KMeanClassifier:
    def __init__(self):
        self._pos = [1.0 for _ in xrange(RUNNING_CYCLE)]
        self._pos_size = 0
        self._neg = [1.0 for _ in xrange(RUNNING_CYCLE)]
        self._neg_size = 0

    def train(self, s, r):          #s-sample,r-result what we've actually observed
        s = np.log(s)
        if r == 1:
            # train positive classifier
            self._pos_size += 1
            self._pos = map(lambda m, x: m + ((x - m) / self._pos_size), self._pos, s)
        else:
            # train negative classifier
            self._neg_size += 1
            self._neg = map(lambda m, x: m + ((x - m) / self._neg_size), self._neg, s)

    def __dist__(self, x, y):
        return np.sqrt((x - y) ** 2)

    def predict(self, s):
        s = np.log(s)
        gamma = 1.0
        return np.mean([math.exp(-gamma * d) for d in map(self.__dist__, s, self._pos)]) \
               / np.mean([math.exp(-gamma * d) for d in map(self.__dist__, s, self._neg)])


class NeuralNetwork:
    def __init__(self, num_inputs, num_outputs,mlp=False):
        self._size_in = num_inputs
        self._size_out = num_outputs
        if not mlp:
            self._w = [self.__gen_layer__(num_inputs,num_outputs)]
            self._setup = True
        else:
            self._setup = False
            self._w = []

    def __gen_layer__(self, in_size, out_size):
        return 2 * np.random.random((in_size, out_size)) - 1

    def add_hidden_layer(self, num_neurons):
        if not self._w:
            self._w.append(self.__gen_layer__(self._size_in, num_neurons))
        else:
            self._w.append(self.__gen_layer__(self._w[-1].shape[1], num_neurons))

    def __sigmoid__(self, x, deriv=False):
        if (deriv == True):
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def train(self, X, y, epochs=1):    #X-input,y-observed result
        if not self._w:
            self._w.append(self.__gen_layer__(self._size_in, self._size_out))
            self._setup = True
        elif not self._setup:
            self._w.append(self.__gen_layer__(self._w[-1].shape[1], self._size_out))
            self._setup = True
        for i in xrange(epochs):
            # propagate forward
            l0 = X
            l1 = [l0]
            for l in range(len(self._w)):
                l0 = self.__sigmoid__(np.dot(l0, self._w[l]))
                l1.append(l0)
            err = y - l0                            #calculate error
            delta = err * self.__sigmoid__(l0, True)#calculate the gradient of the error for the output layer
            if len(self._w) > 1:
                self._w[-1] += l0.T.dot(delta)      #update the output layer's weights
                for j in xrange(len(self._w) - 2, 0, -1):
                    l_err = delta.dot(self._w[j+1].T)#calculate the error for each layer going backwards
                    l_delta = l_err * self.__sigmoid__(l1[j], deriv=True)#calculate the gradient
                    self._w[j] += l1[j].T.dot(l_delta)#update the weight
                    delta = l_delta                    # remember the gradient so we can use it in the next epoch
            else:
                self._w[-1] += np.dot(l0.T, delta)

    def predict(self, X):
        lo = X
        for l in xrange(len(self._w)):
            lo = self.__sigmoid__(np.dot(lo, self._w[l]))
        return lo


class CrawlTimer(threading.Thread):
    # ref:http://stackoverflow.com/questions/9812344/cancellable-threading-timer-in-python
    def __init__(self, wait_for, function, **kwargs):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.fs = [(function, kwargs)] if function else []
        self.timeout = wait_for

    def add_function(self, f, **kwargs):
        self.fs.append((f, kwargs))

    def run(self):
        while not self.event.is_set():
            for i in range(len(self.fs)):
                fx = self.fs[i]
                if fx[1]:
                    fx[0](fx[1])
                else:
                    fx[0]()
            self.event.wait(self.timeout)

    def stop(self):
        self.event.set()