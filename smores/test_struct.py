__author__ = 'tony petrov'
from constants import  *
class MockTwitter:
    def __init__(self):
        self.home_timeline=15
        self.user_list_size=100
        self.list_member_fail=False
        self.create_list_calls=15
        self.create_friends=15
        self.user_suggestions=15
        self.user_suggestions_by_slug=15
        self.credentials=15
        self.user_timeline=180
        self.lookup=TWITTER_MAX_NUM_OF_BULK_LISTS_PER_REQUEST_CYCLE
        self.list_statuses=TWITTER_MAX_NUMBER_OF_LISTS
        self.followers_ids=15
        self.friends_ids=15
        self.followers_list=15
        self.friends_list=15

    def get_followers_ids(self,**kwargs):
        self.followers_ids-=1
        return {'ids':[]}
    def get_friends_ids(self,**kwargs):
        self.friends_ids-=1
        return {'ids':[]}
    def get_friends_list(self,**kwargs):
        self.friends_list-=1
        return {'users':[{'id':1}]}
    def get_followers_list(self,**kwargs):
        self.followers_list-=1
        return {'users':[{'id':1}]}
    def get_home_timeline(self,**kwargs):
        self.home_timeline-=1
        return []
    def create_list_members(self,**kwargs):
        if len(kwargs['user_id'])>self.user_list_size:
            self.list_member_fail=True
        return {'id':5}
    def create_list(self,**kwargs):
        self.create_list_calls-=1
        return {'id':123}
    def create_friendship(self,**kwargs):
        self.create_friends-=1
    def get_user_suggestions(self,**kwargs):
        self.user_suggestions-=1
        return [{'name':i} for i in range(150)]
    def verify_credentials(self,**kwargs):
        self.credentials-=1
        return {'screen_name':123}
    def get_user_suggestions_by_slug(self,**kwargs):
        self.user_suggestions_by_slug-=1
        return {'users':[{'id':i} for i in range(80)]}
    def get_user_timeline(self,**kwargs):
        self.user_timeline-=1
        return []
    def get_list_statuses(self,**kwargs):
        self.list_statuses-=1
        return []
    def lookup_user(self,**kwargs):
        self.lookup-=1
        return []

    def passed(self):
        return len(self.get_failures()) == 0
    def get_failures(self):
        attr=self.__dict__
        return [k for k in attr if (isinstance( attr[k], int )and attr[k]<0) or attr[k]==True]
