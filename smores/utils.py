__author__ = 'tony petrov'

def split_into(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]