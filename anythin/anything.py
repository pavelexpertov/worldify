# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json
# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
CONSUMER_KEY = 'IiLJkqODNtSfT0dcpGAvz0ttM'
CONSUMER_SECRET = 'abkDUeWYCLOZJonN6JyLHfdSgPqN9CsgFQA8E4u4CUDOt45BBL'
ACCESS_TOKEN = '360807471-ZKoVTyHN4nBXsU5HZQHNqNn7Vfdebq9HSV9ko2CH'
ACCESS_SECRET = 'Yw7GD2r8wmEGxjyn5bgBZuKzKqrvVg7mH8Ojw8kO2rVfv'
oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
# Initiate the connection to Twitter Streaming API
twitter = TwitterStream(auth=oauth)
#iterator_happy = twitter.statuses.filter(track="#happy", until="2017-04-19", language="en")
#iterator_angry = twitter.statuses.filter(track="angry", language="en")
# iterator_astonished = twitter.statuses.filter(track="#astonished", language="en")
# iterator_disgusted = twitter.statuses.filter(track="#digusted", language="en")
iterator_sad = twitter.statuses.filter(track="sad", language="en")
# iterator_scared = twitter.statuses.filter(track="#scared", language="en")
iterator_list = [
    iterator_sad
    # iterator_angry, iterator_astonished, iterator_disgusted, iterator_sad, iterator_scared
]
f = open("tweets_dataset_sad.txt", "w+")
tweets_dataset = []
# Print each tweet in the stream to the screen
# Here we set it to stop after getting 1000 tweets.
# You don't have to set it to stop, but can continue running
# the Twitter API to collect data for days or even longer.
try:
    tweet_count = 400
    for i in iterator_list:
        for tweet in i:
            tweet_count -= 1
            # Twitter Python Tool wraps the data returned by Twitter
            # as a TwitterDictResponse object.
            # We convert it back to the JSON format to print/score
            tweets_dataset.append(tweet["text"])
            print(tweet_count, tweet["text"])
            # The command below will do pretty printing for JSON data, try it out
            # print json.dumps(tweet, indent=4)
            if tweet_count <= 0:
                break
except Exception:
    pass
finally:
    print("writing to file")
    f.write(str(tweets_dataset))
