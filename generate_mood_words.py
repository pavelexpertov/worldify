from requests import Session
import os
import random
import string
import json

def generate_words(dataset):
    s = Session()
    s.headers.update({
        "X-API-SECRET-KEY": os.getenv("API_SECRET_KEY"),
        "X-API-KEY": os.getenv("API_KEY")
    })
    r = s.get("https://app.receptiviti.com/v2/api/person/58fc0720935f0e05abe74d44")
    name = "america_" + "".join(random.choice(string.ascii_lowercase) for _ in range(10))

    r = s.post("https://app.receptiviti.com/v2/api/person",
               headers={"Content-Type": "application/json"},
               data=json.dumps({
                   "name": name,
                   "gender": 2,
                   "person_handle": name
               }))

    u_id = r.json()["_id"]

    for data_item in dataset:
        r = s.post("https://app.receptiviti.com/v2/api/person/{0}/contents".format(u_id),
                   headers={"Content-Type": "application/json"},
                   data=json.dumps({
                       "content_source": 1,
                       "content_date": "2017-04-10T21:06:05.146820",
                       "language_content": data_item
                   }))
        print(r)

    r = s.get("https://app.receptiviti.com/v2/api/person/{0}/profile".format(u_id))
    words = []
    for item in r.json()["personality_snapshot"]:
        words.append(item["summary"])
    return words
