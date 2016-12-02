__author__ = 'tony petrov'

#twitter control constants
TESTING=False
POLITENESS_VALUE=2              #how long the worker should sleep for used to prevent twitter from getting overloaded
TWITTER_MAX_LIST_SIZE=5000
TWITTER_MAX_NUMBER_OF_LISTS=900 #180#can be changed to 1000 but retrieval of tweets from all lists not guaranteed
TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS=900 #180
TWITTER_BULK_LIST_SIZE=100
TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE=900 #60
TWITTER_MAX_NUM_OF_REQUESTS_PER_CYCLE=180
TWITTER_MAX_FOLLOW_REQUESTS = 10
TWITTER_ADD_TO_LIST_LIMIT=100
MAX_TWITTER_TRENDS_REQUESTS=15
TWITTER_CYCLES_PER_HOUR=4
TWITTER_CYCLE_DURATION=15
RUNNING_CYCLE = 900  # 15*60seconds
MAX_TWEETS_PER_CYCLE = 25
MAX_TACKABLE_TOPICS = 400
MAX_FOLLOWABLE_USERS = 5000
#storage locations
TWITTER_BULK_LIST_STORAGE='data\\twitter\\bulk_lists'
TWITTER_LIST_STORAGE='data\\twitter\\lists'
TWITTER_USER_STORAGE='data\\twitter\\users'
TWITTER_WALL_STORAGE='data\\twitter\\home'
TWITTER_CANDIDATES_STORAGE='data\\twitter\\remaining'
TWITTER_CREDENTIALS='data\\twitter\\login'
PROXY_LOCATION='data\\proxies'
RANKING_FILTER_CLASSIFIER='data\\classifier'

#other control constants
RANK_RESET_TIME = 600 # every 10 mins

# Model names
TWITTER_STREAMING_BUCKET_MODEL = 'stream'
TWITTER_CYCLE_HARVESTER = 'harvester'
TWITTER_HYBRID_MODEL = 'hybrid'


#Service plugins
TWITTER_PLUGIN_SERVICE=100              #redirect output from all twitter crawler models to the plugin
TWITTER_MODEL_PLUGIN_SERVICE=101        #redirect output from the twitter model to the plugin
TWITTER_STREAMING_PLUGIN_SERVICE=102    #redirect output from the twitter stream api to the plugin