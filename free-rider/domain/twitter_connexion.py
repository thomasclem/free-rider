import tweepy
import json

class tweepyClientConfig():
    CREDENTIAL_PATH = "/Users/thomasclement/dev/free-rider/credentials.json"

    with open(CREDENTIAL_PATH, 'r') as f:
            CRED = json.load(f)

    def __init__(self, cred = CRED):
        self.__dict__ = cred["accounts"][0]


class tweepyClient(tweepyClientConfig):

    def __init__(self):
        super().__init__()
        self.client = tweepy.Client(
                            bearer_token = self.bearer_token,
                            consumer_key = self.api_key,
                            consumer_secret = self.api_key_secret,
                            access_token = self.access_token,
                            access_token_secret = self.access_token_secret
                            )
    

client = tweepyClient().client
#def getself():
        #with open('./config_tweets.json', 'r') as f_search:
        #config_tweets = json.load(f_search)
        
        #query = config_tweets["search"]["query"]
        #max_result = config_tweets["search"]["max_result"] # Need to be between 10 - 100.
        #start_date = config_tweets["search"]["last_time_search"] # Need to be at ISO 8601/RFC 3339 format.


