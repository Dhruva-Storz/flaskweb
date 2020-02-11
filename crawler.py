
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream, API, Cursor
import twittercredentials
import re

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    # def get_user_timeline_tweets(self, num_tweets):
    #     tweets = []
    #     for tweet in Cursor(self.twitter_client.user_timeline, id = self.twitter_user).items(num_tweets):
    #         tweets.append(tweet)
            
    #     return tweets

    def get_tweets_for_keyword(self, keyword, count=10):
        q=str(keyword)
        fetched_tweets = self.twitter_client.search(q, count = count, tweet_mode='extended')
        
        tweets = []

        for tweet_info in Cursor(self.twitter_client.search, q=keyword, lang = 'en', tweet_mode='extended').items(100):
            if 'retweeted_status' in dir(tweet_info):
                tweet=tweet_info.retweeted_status.full_text
            else:
                tweet=tweet_info.full_text
            tweets.append(tweet)

        return tweets


    # def get_friend_list(self, num_friends):
    #     friend_list = []
    #     for friend in Cursor(self.twitter_client.friends).items(num_friends):
    #         friend_list.append(friend)
    #     return friend_list
        
    # def get_home_timeline_tweets(self, num_tweets):
    #     tweets = []
    #     for tweet in Cursor(self.twitter_client.home_timeline).items(num_tweets):
    #         tweets.append(tweet)
    #     return tweets


class TweetCleaner():

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def process_tweets(self, tweets):
        proc_tweets = []
        for tweet in tweets:
            proc_tweets.append(self.clean_tweet(tweet))

        return proc_tweets

    


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twittercredentials.CONSUMER_KEY, twittercredentials.CONSUMER_SECRET)
        auth.set_access_token(twittercredentials.ACCESS_TOKEN, twittercredentials.ACCESS_TOKEN_SECRET)
        return auth

# class TwitterStreamer():
#     """
#     Class for streaming and processing live tweets.
#     """
#     def __init__(self):
#         self.twitter_authenticator = TwitterAuthenticator()

#     def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
#         listener = TwitterListener(fetched_tweets_filename)
#         auth = self.twitter_authenticator.authenticate_twitter_app()
#         stream = Stream(auth, listener)

#         stream.filter(track = hash_tag_list)
	
# class TwitterListener(StreamListener):
#     """
#     Basic listener class
#     """
#     def __init__(self, fetched_tweets_filename):
#         self.fetched_tweets_filename = fetched_tweets_filename 

#     def on_data(self,data):
#         try:
#             print(data)
#             with open(self.fetched_tweets_filename, 'a') as tf:
#                 tf.write(data)
#             print(data)
#         except BaseException as e:
#             print("Error")
#         return True
	
#     def on_error(self, status):
#         if status == 420:
#             # in case rate limit occurs (can get kicked indefinitely if ignored forever)
#             return False
#         print(str(status))


if __name__ == "__main__":
    client = TwitterClient()
    query = "oscars"
    cleaner = TweetCleaner()
    tweets = client.get_tweets_for_keyword(query)
    text = cleaner.process_tweets(tweets)
    print(str(text))
