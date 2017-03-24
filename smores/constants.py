__author__ = 'tony petrov'

DEFAULT_SOCIAL_MEDIA_CYCLE = 3600  # 1 hour since most social media websites have a 1 hour timeout
# tasks
TASK_EXPLORE = 0
TASK_BULK_RETRIEVE = 1
TASK_FETCH_LISTS = 2
TASK_FETCH_USER = 3
TASK_UPDATE_WALL = 4
TASK_FETCH_STREAM = 5
TASK_GET_DASHBOARD = 6
TASK_GET_TAGGED = 7
TASK_GET_BLOG_POSTS = 8
TASK_GET_FACEBOOK_WALL = 9
TASK_FETCH_FACEBOOK_USERS = 10
TASK_TWITTER_SEARCH = 11
TOTAL_TASKS = 12
# twitter control constants

POLITENESS_VALUE = 0.5  # how long the worker should sleep for used to prevent twitter from getting overloaded
TWITTER_MAX_LIST_SIZE = 5000
TWITTER_MAX_NUMBER_OF_LISTS = 900  #can be changed to 1000 but retrieval of tweets from all lists not guaranteed
TWITTER_MAX_NUMBER_OF_NON_FOLLOWED_USERS = 900
TWITTER_BULK_LIST_SIZE = 100
TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE = 900
TWITTER_MAX_NUM_OF_REQUESTS_PER_CYCLE = 180
TWITTER_MAX_FOLLOW_REQUESTS = 10
TWITTER_ADD_TO_LIST_LIMIT = 100
MAX_TWITTER_TRENDS_REQUESTS = 15
TWITTER_CYCLES_PER_HOUR = 4
TWITTER_CYCLE_DURATION = 15
RUNNING_CYCLE = 900  # 15*60seconds
MAX_TWEETS_PER_CYCLE = 25
MAX_TRACKABLE_TOPICS = 400
MAX_FOLLOWABLE_USERS = 5000
# tumblr control
TUMBLR_MAX_REQUESTS_PER_DAY = 5000
TUMBLR_MAX_REQUESTS_PER_HOUR = 250
# facebook control
FACEBOOK_MAX_REQUESTS_PER_HOUR = 200

# storage locations
TWITTER_BULK_LIST_STORAGE = 'data/twitter/bulk_lists'
TWITTER_LIST_STORAGE = 'data/twitter/lists'
TWITTER_USER_STORAGE = 'data/twitter/users'
TWITTER_WALL_STORAGE = 'data/twitter/home'
TWITTER_CANDIDATES_STORAGE = 'data/twitter/remaining'
TWITTER_CREDENTIALS = 'data/twitter/login'
PROXY_LOCATION = 'data/proxies'
RANKING_FILTER_CLASSIFIER = 'data/classifier'
RANKING_FILTER_TOPIC_CLASSIFIER = 'data/topic_classifier'
# Model names
TWITTER_STREAMING_BUCKET_MODEL = 'stream'
TWITTER_CYCLE_HARVESTER = 'harvester'
TWITTER_HYBRID_MODEL = 'hybrid'
TWITTER_STREAMING_HARVESTER_NON_HYBRID = 'both'

# Service plugins
CRAWLER_PLUGIN_SERVICE = 1  # redirect all outputs to the plugin
TWITTER_PLUGIN_SERVICE = 100  # redirect output from all twitter crawler models to the plugin
TWITTER_HARVESTER_PLUGIN_SERVICE = 101  # redirect output from the twitter model to the plugin
TWITTER_STREAMING_PLUGIN_SERVICE = 102  # redirect output from the twitter stream api to the plugin
TUMBLR_PLUGIN_SERVICE = 103  # redirect tumblr output to plugin
FACEBOOK_PLUGIN_SERVICE = 104  # redirect facebook output to plugin


# Ranking Classifiers
PERCEPTRON_CLASSIFIER = 201
DEEP_NEURAL_NETWORK_CLASSIFIER = 202
K_MEANS_CLASSIFIER = 203

# other control constants and variables
TESTING = False
EXPLORING = False
COLLECTING_DATA_ONLY = False
RANK_RESET_TIME = 600  # every 10 mins
TIME_TO_UPDATE_TRENDS = 0
FILTER_STREAM = False
FRESH_TWEETS_ONLY = False # set to true to reduce the number of overlapping tweets
PARTITION_FACTOR = 0.5
TWITTER_ACCOUNTS_COUNT = 1
MIN_TWITTER_STATUSES_COUNT = 150
