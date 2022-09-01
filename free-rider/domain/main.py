from twitter_connexion import client
import datetime
import re
import os
import json

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', 'config_tweets.json'))

HOURS_BACK = 6
DATETIME_NOW = datetime.datetime.now(datetime.timezone.utc)

#Define the starting date of the oldest tweet to get
DATETIME_START = DATETIME_NOW - datetime.timedelta(hours=HOURS_BACK)

#Define the starting date of the newest tweet to get
DATETIME_STOP = DATETIME_START + datetime.timedelta(hours=5)

class ContestTweet():

    def __init__(self, tweet):
        self.id = tweet.id
        self.text = tweet.text.replace("\n", " ")
        self.list = self.text.split(" ")
        self.list_clean = [re.findall(r'(@.*?)[^a-zA-Z_]', e)[0] if len(re.findall(r'(@.*?)[^a-zA-Z_]', e)) > 0 \
                            else e for e in list(map(str.lower, self.list))]
        self.date = tweet.created_at
        self.author_id = tweet.author_id
        #self.author_metrics = tweet.include
        self.entities = tweet.entities
        self.public_metrics = tweet.public_metrics
    
    def check_need_to_follow(self) -> bool:
        """ Check if the contest tweet has a rule about following user.
        """
        self.need_to_follow = "follow" in self.list_clean
        return self.need_to_follow

    def check_need_to_follow_author(self) -> bool:
        """ Check if the contest tweet has a rule about following the author account
        """
        filter_word = ["us", "me", "this", "my"]
        self.need_to_follow_author = len([word for word in self.list_clean if (word in filter_word) and \
                                        (self.list_clean.index(word) - self.list_clean.index("follow") in range(1,3))]) > 0

    def find_accounts_to_follow(self) -> bool:
        """ Find the usernames mentionned in the tweet that we may need to follow.
        """
        #all_accounts_mentioned = re.findall(r'(@.*?)[^a-zA-Z._]', self.text)
        #accounts_to_follow = [account[1:] for account in all_accounts_mentioned if 0 < self.list.index(account) - self.list_clean.index("follow") < 8]
        if "mentions" in self.entities.keys() :
            self.accounts_to_follow = list(set(["@"+dict["id"] for dict in self.entities["mentions"] \
                                        if self.list.index("@"+dict["username"]) - self.list_clean.index("follow") in range(1,8)]))
        else :
            self.accounts_to_follow = []
        #self.accounts_to_follow = [client.get_user(username = account).data.id for account in accounts_to_follow]
        return self.accounts_to_follow

    def check_need_to_retweet(self) -> bool:
        """ Check if the contest tweet has a rule about retweeting.
        """
        retweet_words = ["rt", "retweet"]
        self.need_to_retweet = len([word for word in self.list_clean if word in retweet_words]) > 0
        return self.need_to_retweet

    #TODO: add dynamic metrics validation
    def check_contest_validity(self, metrics: list|str) -> bool:
        """ Check the some parameters about the contest like :
        - like number
        - retweet number
        - comment number
        """
        rule = self.public_metrics["like_count"] > 20
        return self.public_metrics["like_count"]

#TODO : finish main
def main():
    with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)

start_time = "2022-08-16T09:00:00Z"

tweets = client.search_recent_tweets("giveaway OR contest -RT -is:retweet -is:reply -NFT -nft -#NFT -#nft", 
                                    start_time = DATETIME_START,
                                    end_time = DATETIME_STOP,
                                    sort_order = "relevancy",
                                    expansions= "author_id",
                                    tweet_fields = ["created_at", "author_id", "entities", "public_metrics"],
                                    user_fields = "public_metrics",
                                    max_results = 100
                                    )

tweets_fr = client.search_recent_tweets("concours -RT -is:retweet -is:reply", 
                                    start_time = DATETIME_START,
                                    end_time = DATETIME_STOP,
                                    sort_order = "relevancy",
                                    expansions= "author_id",
                                    tweet_fields = ["created_at", "author_id", "entities", "public_metrics"],
                                    user_fields = "public_metrics",
                                    max_results = 100
                                    )
 

tweets_obj = [ContestTweet(t) for t in tweets.data]
tweets_fr_obj = [ContestTweet(t) for t in tweets_fr.data]

for tweet in tweets_obj:
    tweet.check_contest_validity()