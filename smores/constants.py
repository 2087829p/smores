__author__ = 'tony petrov'

TESTING=False
POLITENESS_VALUE=2              #how long the worker should sleep for used to prevent twitter from getting overloaded
TWITTER_MAX_LIST_SIZE=5000
TWITTER_MAX_NUMBER_OF_LISTS=180#can be changed to 1000 but retrieval of tweets from all lists not guaranteed
TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS=180
TWITTER_BULK_LIST_SIZE=100
TWITTER_MAX_NUM_OF_BULK_LISTS=60
TWITTER_MAX_NUM_OF_REQUESTS_PER_CYCLE=180
TWITTER_ADD_TO_LIST_LIMIT=100
MAX_TWITTER_TRENDS_REQUESTS=15
TWITTER_CYCLES_PER_HOUR=4
TWITTER_CYCLE_DURATION=15
#storage locations
TWITTER_BULK_LIST_STORAGE='data\\twitter\\bulk_lists'
TWITTER_LIST_STORAGE='data\\twitter\\lists'
TWITTER_USER_STORAGE='data\\twitter\\users'
TWITTER_WALL_STORAGE='data\\twitter\\home'
TWITTER_CANDIDATES_STORAGE='data\\twitter\\remaining'
TWITTER_CREDENTIALS='data\\twitter\\login'
PROXY_LOCATION='data\\proxies'

#Service plugins
TWITTER_PLUGIN_SERVICE=100              #redirect output from all twitter crawler models to the plugin
TWITTER_MODEL_PLUGIN_SERVICE=101        #redirect output from the twitter model to the plugin
TWITTER_STREAMING_PLUGIN_SERVICE=102    #redirect output from the twitter stream api to the plugin