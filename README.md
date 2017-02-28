# smores
Yet another social media crawler but this one comes with smores!!
The Smores crawler is a student project written in Python.
Its main goal is to create an efficient social media crawler that will hopefully be of use

## Capabilities and Usage
To start the crawler you can simply call the `crawl` method or you can instance your own scheduler like so
``` python
from smores.scheduler import Scheduler

scheduler = Scheduler()
scheduler.start()
```
Use the `use` argument to specify which sites should be crawled. The smores crawler currently can crawl Twitter, Tumblr and Facebook. 
The data crawled can be filtered via filters in order to add a filter to the crawler you must extend the `smores.storage.Filter` interface and
override the `process` method
``` python
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
``` python
 myfilter = MyFilter(service, store, filters)
 scheduler.register(myfilter)
```
In order for the crawler to work all accounts and API tokens need to be specified in the `smores\data\longin` file whith the following structure:
```
[site:<SITE NAME(e.g twitter)>,oauth_token:<TOKEN>,oauth_secret:<SECRET>....etc]
```
It is strongly recommended that the `explore()` function from the `__init__.py` file is ran and the crawler is left to work for a few days in order to build a sufficiently large database of twitter users, which can be followed.
## Requirements:
Twython - https://twython.readthedocs.io/en/latest/usage/install.html <br />
pymongo - http://api.mongodb.com/python/current/installation.html<br />
concurrent.futures - https://pypi.python.org/pypi/futures <br />
numpy - https://docs.scipy.org/doc/numpy/user/install.html <br />
facebook graph api - https://facebook-sdk.readthedocs.io/en/latest/index.html <br />
pytumblr - https://facebook-sdk.readthedocs.io/en/latest/index.html <br />

## Notes
In order to use facebook you need to have an access token which can be obtained from here https://developers.facebook.com/tools/explorer/
