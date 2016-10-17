__author__ = 'tony petrov'

import os
import pickle
def __abs_path__(fl):
    curr_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(curr_dir, fl)
    return abs_file_path
def load_data(f):
    data=None
    file_path=__abs_path__(f)
    with open(file_path,'rb') as handle:
        data=pickle.load(handle)
    return data
def save_data(data,fl):
    file_path=__abs_path__(fl)
    with open(file_path,'wb') as handle:
        pickle.dump(data,handle)


class Filter:
    def __init__(self,name):
        self._name=name
    def accept(self,data):
        raise NotImplementedError( "The accept function must be implemented!!" )
    def process(self,data):
        pass
