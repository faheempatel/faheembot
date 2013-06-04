import os
import re
import praw
import json
import config
import requests
import pywunder
from twython import Twython
from rottentomatoes import RT

# TWITTER 
OAUTH_TOKEN  = config.OAUTH_TOKEN
OAUTH_SECRET = config.OAUTH_SECRET
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET

t = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)	

# WUNDERGROUND
W_KEY  = config.W_KEY
wunder = pywunder.Client(W_KEY)

# ROTTEN TOMATOES
RT_KEY = config.RT_KEY
rt = RT(RT_KEY)

# REDDIT
r = praw.Reddit(user_agent="faheembot")

def rate(movie):
	rating = rt.search(movie)[0]['ratings']['critics_score']
	return str(rating)

def make_me_laugh():
	result = r.get_subreddit('funny').get_top(limit=1)
	return [str(post.short_link) for post in result][0]

def weather(location):
	url = "http://autocomplete.wunderground.com/aq?query=%s" % location
	returned_json = requests.get(url).json()
	coordinates = returned_json['RESULTS'][0]['zmw']
	
	url = "http://api.wunderground.com/api/%s/forecast/q/zmw:%s.json" % (W_KEY, coordinates)
	result = requests.get(url).json()
    
	return result['forecast']["txt_forecast"]["forecastday"][0]["fcttext"]


movie_regex = "@\w+ rate "
weather_regex = "@\w+ weather for "
laugh_regex = "@\w+ make me laugh"

request = t.get_mentions_timeline()[0]['text'].lower()
username = str("@" + t.get_mentions_timeline()[0]["user"]["screen_name"])

if re.match(movie_regex, request):
	movie = re.sub(movie_regex, '', request)
	response = "%s %s is a %s/100" % (username, movie, rate(movie))
	t.update_status(status = response)
elif re.match(weather_regex, request):
	location = re.sub(weather_regex, '', request)
	response = "%s %s" % (username, weather(location))
	t.update_status(status = response)
elif re.match(laugh_regex, request):
	response = "%s Oh you've gotta see this: %s" % (username, make_me_laugh())
	t.update_status(status = response)

