import json
import time
import os
import re
import string
import tweepy
import numpy as np

def remove_non_ascii(s):
    rep = ['"', '(', ')']
    s = s.replace('’', '\'')
    for i in rep:
        s = s.replace(i, '')
    printable = list(string.printable)
    return "".join(filter(lambda x: x in printable, s))

def split_tweet(observation, sighting_info, only_obs=False, numbered=True, max_length=235):
    o = ""
    observation = remove_non_ascii(observation)
    observation = re.sub(r'(?<=[.,])(?=[^\s^\.])', r' ', observation)
    obs_split = observation.split(". ")
    for i in range(1,len(obs_split)):
        o += obs_split[i].capitalize() + ". "
    observation = obs_split[0] + ". " + o
    obs_split = observation.split(' ')
    obs_list, sighting_list, tweet_list, numbered_tweets = [], [], [], []
    s = ""
    for val in obs_split:
        if len(s) < max_length:
            word = val + " "
            s += word
        else:
            obs_list.append(s)
            _ = val + " "
            s = _
    obs_list.append(s)
    if only_obs:
        obs_list[0] = "".join(obs_list[0].split(": ")[1:])
    else:
        sighting_list = []
        s = ""
        sighting_info = remove_non_ascii(sighting_info)
        for i in sighting_info:
            if len(s) < max_length:
                _ = i + "\n"
                s += _
            if len(s) > max_length:
                s = s.replace(_, "")
                sighting_list.append(s)
                s = "" + i
        sighting_list.append(s)
        sighting_list[0] = sighting_list[0][:-1]
        for i in sighting_list:
            tweet_list.append(i)
    for j in obs_list:
        tweet_list.append(j)
    if numbered:
        for i in range(len(tweet_list)):
            numbered_tweets.append(tweet_list[i] + " ({}/{})".format(i+1, len(tweet_list)))
        return numbered_tweets
    else:
        return tweet_list

def tweet():
    with open("data/auth.json") as f:
        keys = json.load(f)
    f.close()

    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"]) 
    
    # authentication of access token and secret 
    auth.set_access_token(keys["access_token"], keys["access_token_secret"]) 
    api = tweepy.API(auth) 

    with open("generated_sightings.json") as f:
        data = json.load(f)

    # key of the random entry
    random_key = np.random.choice(list(data.keys()))

    random_sighting = data[random_key]

    sighting_info = ["SEASON: {season}".format(season=random_sighting["SEASON: "]),
    "STATE: {state}".format(state=random_sighting["STATE: "]),
    "NEAREST TOWN: {nearest_town}".format(nearest_town=random_sighting["NEAREST TOWN: "]),
    "NEAREST ROAD: {nearest_road}".format(nearest_road=random_sighting["NEAREST ROAD: "]),
    "ENVIRONMENT: {env}".format(env=random_sighting["ENVIRONMENT: "]),
    "TIME AND CONDITIONS: {tc}".format(tc=random_sighting["TIME AND CONDITIONS: "])]

    observation = """OBSERVATION: {obs}""".format(obs=random_sighting["OBSERVATION: "])

    # delete sighting from JSON file
    del data[random_key]
    with open("generated_sightings.json", "w") as f:
        data = json.dump(data, f, indent=4, sort_keys=False)

    split_tweets = split_tweet(observation, sighting_info, only_obs=True)

    with open("my_tweet.txt", "w") as f:
        f.write(split_tweets[0])
    with open('my_tweet.txt','r') as f:
        tweet = api.update_status(f.read())
    for i in range(1,len(split_tweets)):
        with open("my_tweet.txt", "w") as f:
            f.write(split_tweets[i])
        with open('my_tweet.txt','r') as f:
            tweet = api.update_status(f.read(), in_reply_to_status_id = tweet.id_str)
        time.sleep(5)

if __name__ == "__main__":
    while True:
        tweet()
        time.sleep(14400)