# Import the necessary package to process data in JSON format
import json
import simplejson as json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

LOCATIONS = {
    "america": "-120.585938,37.523665,-65.742188,66.273928",
    "europe": "-11.953125,32.931237, 30.234375,61.656507",
    "africa": "-11.250000,-34.799369, 44.296875,32.931237",
    "australia": "117.773438,-36.513172, 152.226563,-13.479384",
    "asia": "48.515625,15.724580, 157.148438,76.622967"
}

def get_dataset(location="europe", num_of_tweets=500):
    location = LOCATIONS[location]

    CONSUMER_KEY = 'IiLJkqODNtSfT0dcpGAvz0ttM'
    CONSUMER_SECRET = 'abkDUeWYCLOZJonN6JyLHfdSgPqN9CsgFQA8E4u4CUDOt45BBL'

    ACCESS_TOKEN = '360807471-ZKoVTyHN4nBXsU5HZQHNqNn7Vfdebq9HSV9ko2CH'
    ACCESS_SECRET = 'Yw7GD2r8wmEGxjyn5bgBZuKzKqrvVg7mH8Ojw8kO2rVfv'

    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    twitter = TwitterStream(auth=oauth)

    iterator = twitter.statuses.filter(locations=location, language="en")

    iterator_list = [
        iterator
    ]

    tweets_dataset = []

    try:
        for i in iterator_list:
            tweet_count = num_of_tweets
            for tweet in i:
                if "RT @" not in tweet["text"]:
                    tweets_dataset.append(tweet["text"])
                    tweet_count -= 1
                    print tweet["text"]

                if tweet_count == 0:
                    break
    except Exception:
        pass
    return tweets_dataset
