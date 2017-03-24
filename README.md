# smores
Yet another social media crawler but this one comes with smores!!
The Smores crawler is a student project written in Python.
Its main goal is to create an efficient social media crawler that will hopefully be of use
to researchers. The system offers 3 different architectures for crawling: 
Harvester, Streaming and Hybrid. Use the Harvester architecture to crawl data from a fixed
user database. Use the Streaming architecture to crawl live data from Twitter's streaming API.
The Hybrid architecture offers 3 different classifiers: perceptron,DNN and KMeans in order to maximize the
tweet yield.

## Usage
In order for the crawler to work all accounts and API tokens need to be specified in the `smores\data\longin` file whith the following structure:
```
[site:<SITE NAME(e.g twitter)>,oauth_token:<TOKEN>,oauth_secret:<SECRET>....etc]
```
To start the crawler you can simply call the `crawl` method or you can instance your own scheduler like so
```python
from smores.scheduler import Scheduler

scheduler = Scheduler()
scheduler.start()
```
Use the `use` argument to specify which sites should be crawled. The smores crawler currently can crawl Twitter, Tumblr and Facebook. 
The data crawled can be filtered via filters in order to add a filter to the crawler you must extend the `smores.storage.Filter` interface and
override the `process` method
```python
import smores.storage as st
class MyFilter(st.Filter):
    def process(self,data):
        #your code goes here
```
In order to initialize your new filter you must provide it with the following arguments `service, store` and `filters`.
The `service` argument tells the scheduler which output to divert to the new filter. For instance the `smores.constants.TWITTER_PLUGIN_SERVICE` tag will instruct the scheduler and pipeline to divert all data crawled from twitter to this filter. A full list of all services can be found below:
``` python
CRAWLER_PLUGIN_SERVICE              # redirect all outputs to the plugin
TWITTER_PLUGIN_SERVICE              # redirect output from all twitter crawler models to the plugin
TWITTER_HARVESTER_PLUGIN_SERVICE    # redirect output from the twitter model to the plugin
TWITTER_STREAMING_PLUGIN_SERVICE    # redirect output from the twitter stream api to the plugin
TUMBLR_PLUGIN_SERVICE               # redirect tumblr output to plugin
FACEBOOK_PLUGIN_SERVICE             # redirect facebook output to plugin
```
The `store` argument is just a function to which the processed data will be passed. The `filters` argument is a list of filters to which the processed data must be passed after this filter is done processing. 
After extending the `smores.storage.Filter` interface your new plugin can be added to the crawler by passing it as an argument
to the `crawl` function or by registering it with an instance of `smores.scheduler.Scheduler` like so
```python
 myfilter = MyFilter(service, store, filters)
 scheduler.register(myfilter)
```
To override the default storage you can either pass your own write function to the scheduler using the storage option of the 
scheduler constructor like so
```python
from smore.scheduler import Scheduler
scheduler = Scheduler(storage=MyStoreFunction)
```
To specify which architecture to be used by the crawler use the use argument of the scheduler constructor.
```python
from smores.constants import *
from smores.scheduler import scheduler
scheduler = Scheduler(use=TWITTER_CYCLE_HARVESTER)

#Model names found in smores.constants
TWITTER_STREAMING_BUCKET_MODEL # streaming architecture
TWITTER_CYCLE_HARVESTER        # harvester architecture
TWITTER_HYBRID_MODEL           # hybrid model using a classifier
TWITTER_STREAMING_HARVESTER_NON_HYBRID # hybrid model not using a classifier
```
To specify a which classifier to be used with the hybrid use the classifier argument of the scheduler
```python
from smores.constants import *
from smores.scheduler import scheduler
scheduler = Scheduler(classifier=PERCEPTRON_CLASSIFIER)

#Model names found in smores.constants
PERCEPTRON_CLASSIFIER
DEEP_NEURAL_NETWORK_CLASSIFIER
K_MEANS_CLASSIFIER
```
Other scheduler parameters not metioned above can be found below:
|Argument     |Accepted object |Functoion     |
|-------------|----------------|--------------|
|`sites`      |`list of string`|`intructs the crawler which platforms to collect data from`|
|`multicore`  |`boolean`       |`if set to True the crawler will use more than 1 thread to crawl`|
|`trends`     |`list of string`|`specifies a list of topics to be followed on twitter`|
|`tumblr_tags`|`list of string`|`specifies a list of topics to be followed on tumblr`|
|`fb_users`   |`list of string`|`specifies a list of names of facebook users to be followed`|
|`blogs`      |`list of string`|`specified a list of tumblr blogs for which data should be colledted`|
|`ip`         |`string`        |`specifies the ip of the MongoDB server where data should be stored`|
|`port`       |`int`           |`specifies the port of the MongoDB server`|

In order to change the number minimum threshold for tweets that user must have in order to be added to the database simply change the value of the 
MIN_TWITTER_STATUSES_COUNT before running the scheduler like so:
```python
import constants as c
c.MIN_TWITTER_STATUSES_COUNT = #whatever value you want
```
Other control variables and their function can be seen below:
|Variable              |Function|
|:---------------------|:-------|
|`COLLECTING_DATA_ONLY`|`if set to true the crawler will not find new users to follow on Twitter`|
|`EXPLORING`           |`if set to true the crawler will not collect any data and will only find new users to add to its database`|
|`TESTING`             |`if set to true the crawler will not send requests to Twitter but instead use the MockTwitter application`|
|`RANK_RESET_TIME`     |`integer value used to tell the Ranking Filter how many seconds to gather data for before training`|
|`FILTER_STREAM`       |`if set to true the crawler will use its topics to filter tweets coming from the Twitter Streaming API`|
|`PARTITION_FACTOR`    |`float value used to tell the crawler what portion of the users predicted to be active can be crawled in the next cycle`|

It is strongly recommended that the `explore()` function from the `__init__.py` file is ran and the crawler is left to work for a few days in order to build a sufficiently large database of twitter users.
## Requirements:
Twython - https://twython.readthedocs.io/en/latest/usage/install.html <br />
pymongo - http://api.mongodb.com/python/current/installation.html<br />
concurrent.futures - https://pypi.python.org/pypi/futures <br />
numpy - https://docs.scipy.org/doc/numpy/user/install.html <br />
facebook graph api - https://facebook-sdk.readthedocs.io/en/latest/index.html <br />
pytumblr - https://github.com/tumblr/pytumblr <br />

## Notes
In order to use facebook you need to have an access token which can be obtained from here 
https://developers.facebook.com/tools/explorer/

To reduce the amount of retweets set the FRESH_TWEETS_ONLY variable before starting the scheduler
```python
import smores.constants as c
c.FRESH_TWEETS_ONLY = True
```
