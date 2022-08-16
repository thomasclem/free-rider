from twitter_connexion import client
import datetime
import re

DATETIME_NOW = datetime.datetime.now(datetime.timezone.utc)

class ContestTweet():

    def __init__(self,tweet):
        self.id = tweet.id
        self.text = re.sub('[^A-Za-z0-9]+', ' ', tweet.text)
        self.list = self.text.split(" ")
        self.list_lower = list(map(str.lower, self.list))
        self.date = tweet.created_at
        self.author_id = tweet.author_id
    
    def check_need_to_follow(self):
        """ Check if the contest tweet has a rule about following user.
        """
        self.need_to_follow = "follow" in self.list_lower
        return self.need_to_follow

    def find_accounts_to_follow(self):
        """ Find the usernames mentionned in the tweet that we may need to follow.
        """
        all_accounts_mentioned = [account for account in self.list if account.startswith("@")]
        accounts_to_follow = [account[1:] for account in all_accounts_mentioned if self.list.index(account) > self.list_lower.index("follow")]
        self.accounts_to_follow = [client.get_user(username = account) for account in accounts_to_follow]

    def check_need_to_retweet(self):
        """ Check if the contest tweet has a rule about retweeting.
        """
        retweet_words = ["rt", "retweet"]
        self.need_to_retweet = len([word for word in self.list_lower if word in retweet_words]) > 0
        return self.need_to_retweet

    

start_time = "2022-08-16T09:00:00Z"


tweets = client.search_recent_tweets("follow retweet contest -RT -is:retweet", 
                                    start_time = start_time, tweet_fields = ["created_at", "author_id"], max_results = 20)
tweets 

tweet = ContestTweet(tweets.data[9])
tweet.find_accounts_to_follow()
tweet.list