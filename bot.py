import os
import re
import praw
import config
import datetime
from twython import Twython
from rottentomatoes import RT
from pygeocoder import Geocoder
from forecastio import Forecastio

# TWITTER 
OAUTH_TOKEN  = config.OAUTH_TOKEN
OAUTH_SECRET = config.OAUTH_SECRET
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET

t = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)    

# FORECAST.IO
forecast = Forecastio(config.F_KEY)

# ROTTEN TOMATOES
rt = RT(config.RT_KEY)

# REDDIT
r = praw.Reddit(user_agent="faheembot")

def rate(movie):
    rating = rt.search(movie)[0]['ratings']['critics_score']
    return str(rating)

def make_me_laugh():
    result = r.get_subreddit('funny').get_top(limit=1)
    return [str(post.short_link) for post in result][0]

def weather(location):
    results = Geocoder.geocode(location)
    coordinates = results[0].coordinates
    lon, lat = coordinates

    forecast.load_forecast(lon, lat, time=datetime.datetime.now(), units="si")
    byDay = forecast.get_daily()

    report = [[day.temperatureMin, day.temperatureMax, day.summary] for day in byDay.data]

    return sum(report, [])


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
    report = weather(location)
    response = "%s Min: %s\nMax: %s\n%s" % (username, report[0], report[1], report[2])
    t.update_status(status = response)

elif re.match(laugh_regex, request):
    response = "%s Oh you've gotta see this: %s" % (username, make_me_laugh())
    t.update_status(status = response)

