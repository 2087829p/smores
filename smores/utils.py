__author__ = 'tony petrov'
import threading
import numpy as np
from constants import *
import math
import time


def split_into(l, n):
    'Splits the list into smaller lists with n elements each'
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def fit_in_range(min, max, x):
    return (x - min) / (max - min)

get_tweet_timestamp = lambda t:time.mktime(time.strptime(t["created_at"], "%a %b %d %H:%M:%S +0000 %Y"))
flatten = lambda l: [i for sl in l for i in sl]
user_filter = lambda x:filter(lambda y:y['protected']==False and y['statuses_count']>150,x)
class KMeanClassifier:
    def __init__(self):
        self._pos = [0.0 for i in range(RUNNING_CYCLE)]
        self._pos_size = 0
        self._neg = [0.0 for i in range(RUNNING_CYCLE)]
        self._neg_size = 0

    def train(self, s, r):
        s = np.log(s)
        if r == 1:
            # train positive classifier
            self._pos_size += 1
            self._pos = map(lambda m, x: m + ((x - m) / self._pos_size), self._pos, s)
        else:
            # train negative classifier
            self._neg_size += 1
            self._pos = map(lambda m, x: m + ((x - m) / self._neg_size), self._neg, s)

    def __dist__(self, x, y):
        return np.sqrt((x - y) ** 2)

    def predict(self, s):
        s = np.log(s)
        # s = map(lambda x:math.log(x),s)
        gamma = 1.0
        return np.mean([math.exp(-gamma * d) for d in map(self.__dist__, s, self._pos)]) \
               / np.mean([math.exp(-gamma * d) for d in map(self.__dist__, s, self._neg)])


class NeuralNetwork:
    def __init__(self, num_inputs, num_outputs):
        self._size_in = num_inputs
        self._size_out = num_outputs
        self._w = []
        self._setup = False

    def __gen_layer__(self, in_size, out_size):
        return 2 * np.random.random((in_size, out_size)) - 1

    def add_hidden_layer(self, num_neurons):
        if not self._w:
            self._w.append(self.__gen_layer__(self._size_in, num_neurons))
        else:
            self._w.append(self.__gen_layer__(len(self._w[-1]), num_neurons))

    def __sigmoid__(self, x, deriv=False):
        if (deriv == True):
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def train(self, X, y, epochs=1):
        if not self._w:
            self._w.append(self.__gen_layer__(self._size_in, self._size_out))
            self._setup = True
        elif not self._setup:
            self._w.append(self.__gen_layer__(self._w[-1].shape[1], self._size_out))
            self._setup = True
        for i in range(epochs):
            # propagate forward
            lo = X
            # lo = self.__sigmoid__(np.dot(lo,self._w[0]))
            l1 = [lo]
            for l in range(len(self._w)):
                lo = self.__sigmoid__(np.dot(lo, self._w[l]))
                l1.append(lo)
            err = y - lo
            delta = err * self.__sigmoid__(lo, True)
            if len(self._w) > 1:
                self._w[-1] += lo.T.dot(delta)
                for j in range(len(self._w) - 1, 0, -1):
                    l_err = delta.dot(self._w[j].T)
                    l_delta = l_err * self.__sigmoid__(l1[j], deriv=True)
                    self._w[j] += l1[j].T.dot(l_delta)
            else:
                self._w[-1] += np.dot(lo.T, delta)

    def predict(self, X):
        lo = X
        for l in range(len(self._w)):
            lo = self.__sigmoid__(np.dot(lo, self._w[l]))
        return lo


class CrawlTimer(threading.Thread):
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