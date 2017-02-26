__author__ = 'tony petrov'
from storage import Filter
from nltk.tag import StanfordNERTagger
from math import *
from utils import *
from collections import Counter
from scheduler import Scheduler
model_path = "E:/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz"
jar_path = "E:/stanford-ner/stanford-ner.jar"
BURST_LENGTH_SCALE = 1.5

class WordStatsCollector:
    def __init__(self,size,period):
        self._size = size
        self._period_length = period * 3600
        self._words = Counter()
        self._last_update = time.time()
    def add_doc(self,doc):
        self._words += Counter(doc)
    def is_ready_to_update(self):
        return self._last_update + self._period_length >= time.time()
    def update(self):
        self._words = Counter()
        self._last_update = time.time()
    def get_negative_dictionary(self):
        words = self._words.most_common()
        neg_words = []
        for i in xrange(len(words)):
            if words[i][1]*i>0.1:
                neg_words.append(words[i][0])
        return neg_words
        #return set(w[0] for w in self._words.most_common(self._size))


class Cluster:
    def __init__(self,a,b):
        self._items = [a,b]
        self._centroid = np.mean([get_tweet_timestamp(a),get_tweet_timestamp(b)])

    def add(self,tweet):
        self._items.append(tweet)
        self._centroid += (get_tweet_timestamp(tweet) - self._centroid)/self.size()
    def size(self):
        return len(self._items)
    def entities(self):
        """Returns the number of times each entity is mentioned in all the tweets in the cluster"""
        return Counter([t['ner_tags'] for t in self._items])

class BurstWindow:
    def __init__(self,length):
        self._mean = 0.0
        self._dev = 0.0
        self._s = [0.0 for i in range(3)]
        self._last_burst = 0
        self._length = length
        self._last_update = time.time()

    def add(self,t):
        for i in range(len(self._s)):
            self._s[i] += pow(get_tweet_timestamp(t),i)

    def is_bursting(self):
        return self._mean != 0 and self._s[0] > 3*self._dev + self._mean

    def update(self):
        now = time.time()
        # check if its time to actually update
        if now < self._last_update+self._length*60:
            return
        # check if we are in burst mode
        if self._last_burst + (BURST_LENGTH_SCALE * self._length * 60) > now:
            return
        # check if the cluster is bursting
        if self.is_bursting():
            self._last_burst = now
            return
        s = self._s
        self._dev = sqrt((s[2] - s[1]*s[1])/s[0])
        self._mean = s[1]/s[0]

class Preprocessor(Filter):
    def __init__(self, service, store, filters,stopwords=set(),dict_update_period=1,dict_size=400):
        super(Preprocessor, self).__init__(service, store, filters)
        self.tagger = StanfordNERTagger(model_path,jar_path)
        self._stopwords = stopwords
        self._stopword_counter = WordStatsCollector(dict_size,dict_update_period) if stopwords else None

    def __process_using_ner__(self,data):
        output = []
        filtr = lambda x: x if x[1] == 'PERSON' else None
        for t in data:
            text = t['text'].split()
            tags = self.tagger.tag(text)
            if any(filter(filtr,tags)):
                if not t['retweeted'] and not any(w in 'listen follow watch' for w in text):
                    t['ner_tags'] = [t[0] for t in tags]
                    output.append(t)
        return output
    def __process_using_neg_dict__(self,data):
        output = []
        for t in data:
            text = t['text'].split()
            tags = set(text).difference(self._stopwords)
            self._stopword_counter.add_doc(text)
            if self._stopword_counter.is_ready_to_update():
                self._stopwords = self._stopword_counter.get_negative_dictionary()
                self._stopword_counter.update()
            if tags:
                if not t['retweeted']:
                    t['ner_tags'] = [t[0] for t in tags]
                    output.append(t)
        return output

    def process(self, data):
        using_stopwords = len(self._stopwords) != 0
        # remove non English tweets
        data = filter(lambda x:x.get('metadata',{'iso_language_code':'nen'}).get('iso_language_code','nen')=='en'
                               and all_ascii(x.get('text','')),data)
        if using_stopwords:
            return self.__process_using_neg_dict__(data)
        else:
            return self.__process_using_ner__(data)



class Clusterer(Filter):
    def __init__(self, service, store, filters,threshold = 0.5,max_docs=200):
        super(Clusterer, self).__init__(service, store, filters)
        self._inv_index = dict()
        self._threshold = threshold
        self._clusters = dict()
        self._burst_windows = dict()
        self._max_docs = max_docs
        self._events = dict()
        self._merged = list()
        self._current_cluster_id = 0
    def __tf__(self,t, d):
        doc = d.lower().split()
        return doc.count(t.lower()) / float(len(doc))
    def __idf__(self,t, docs):
        N = 0
        for d in docs:
            if t.lower() in d.lower().split():
                N += 1
        Dc = float(len(docs))
        return log(((Dc-N)+0.5)/(N+0.5))   # using the double normalized version of idf to prevent division by 0 and log of infinity
    def cos_dist(self,doc,tweet,col):
        """Computes the cosine similarity score between a tweet and a doc"""
        MAX_TAKE = 10
        v1 = [(x,self.__tf__(x,doc)*self.__idf__(x,col)) for x in set(doc.split())]
        v2 = [(x,self.__tf__(x,tweet)*self.__idf__(x,col)) for x in set(tweet.split())]
        v2.sort(key=lambda x:x[1],reverse=True)
        # determine how many words to compare max is 10
        take = min(MAX_TAKE,min(len(v2),len(v1)))
        v2 = v2[:take]
        vd = dict(v1)
        v1 = [vd[v[0]] if v[0] in vd else 0.0 for v in v2 ]
        v2 = [v[1] for v in v2]
        return np.dot(v1, v2) / (np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))

    def find_max_match(self,tweet,col):
        """Finds the doc in the collection with the highest cosine similarity score"""
        best_doc = None
        best_score = 0
        for d in col:
            score = self.cos_dist(d['text'],tweet,col)
            if score > best_score:
                best_score = score
                best_doc = d
        return best_doc,best_score

    def merge_events(self):
        for e in self._events:
            e_items = Counter()
            total_tweets = 0
            # count the occurrences of each named entity in all clusters of event e
            for i in xrange(len(self._events[e])):
                e_items += self._events[e][i].entities()
                total_tweets += self._events[e][i].size()
            linked = list(e)
            # go through the entities with the highest mention count
            for i in e_items.most_common():
                # if entity i is mentioned in at least 50% of all tweets in the clusters make a link between it and e
                if i[1]/float(total_tweets) >= 0.5:
                    linked.append(i[0])
                else:
                    break
            self._merged.append(linked)


    def get_next_cluster_id(self):
        self._current_cluster_id += 1
        return self._current_cluster_id
    def process(self, data):
        for t in data:
            for nt in t['ner_tags']:
                if nt not in self._inv_index:
                    self._inv_index[nt] = [t]
                    self._burst_windows[nt] = [BurstWindow(5*2**i) for i in range(7)]
                else:
                    e = self._inv_index[nt][:self._max_docs]
                    tx = t['text']
                    match = self.find_max_match(tx,e)
                    if match[1] > self._threshold:
                        self._inv_index[nt].append(t)
                        cluster_id = match[0].get('cluster',-1)
                        if cluster_id > -1:
                            self._clusters.get([nt],[])[cluster_id].add(t)
                            #e.append(self._clusters[-1])
                        else:
                            cluster_id = self.get_next_cluster_id()
                            match[0]['cluster'] = cluster_id
                            cluster = self._clusters.get(nt,[])
                            cluster.append(Cluster(t,match[0]))
                        t['cluster'] = cluster_id
                        for w in self._burst_windows[nt]:
                            w.add(t)
                            w.update()
                            if w.is_bursting():
                                self._events[nt] = [c for c in self._clusters[nt] if c.size() > 10]
        self.merge_events()



def run_algo():
    import os
    java_path = "C:/Program Files/Java/jdk1.8.0_25/bin/java.exe"
    os.environ['JAVAHOME'] = java_path
    preproc = Preprocessor(TWITTER_PLUGIN_SERVICE,None,[])
    clusterer = Clusterer(CRAWLER_PLUGIN_SERVICE,None,[])
    preproc.register_plugin(clusterer)
    s = Scheduler(plugins=[preproc],storage=lambda x:x)
    s.start()
