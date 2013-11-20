import re
import praw
import config
import datetime
from twython import Twython
from rottentomatoes import RT
from pygeocoder import Geocoder
from forecastio import Forecastio

# TWITTER
T = Twython(
        config.CONSUMER_KEY,
        config.CONSUMER_SECRET,
        config.OAUTH_TOKEN,
        config.OAUTH_SECRET
        )    

# FORECAST.IO
F = Forecastio(config.F_KEY)

# ROTTEN TOMATOES
RT = RT(config.RT_KEY)

# REDDIT
R = praw.Reddit(user_agent="faheembot")

def get_movie_rating(movie):
    """Returns a Rotten Tomatoes score for the given movie title"""

    try: 
        json = RT.search(movie)[0]
        title = json['title'] 
        rating = json['ratings']['critics_score']
        return (title, rating)
    except IndexError:
        return None

def get_top_link(tweet, regex):
    """Returns the top link for the given subreddit"""

    subreddit = re.sub(regex, r"\1", tweet)
    result = R.get_subreddit(subreddit).get_top(limit=1)
    top_post = result.next()
    return top_post.short_link

def get_weather(location):
    """Returns today's forecast for the given location"""

    # Find latitude and longitude values
    results = Geocoder.geocode(location)
    name_of_place_found = str(results[0])
    coordinates = results[0].coordinates
    lat, lon = coordinates

    # Get forecast
    F.load_forecast(
            lat,
            lon,
            time=datetime.datetime.now(),
            units="si"
            )

    current = F.get_currently()
    week = F.get_daily()
    today = week.data[0]

    report = (
            name_of_place_found,
            current.temperature,
            today.temperatureMax,
            today.summary
            )

    return report

def tweet_rating(regex, tweet, tweet_id, username):
    """Replies with a movie rating"""

    movie = re.sub(regex, '', tweet)
    result = get_movie_rating(movie)

    if result:
        title, rating = result
        response = "%s %s is rated %s/100" % (username, title, rating)
        T.update_status(
            status = response,
            in_reply_to_status_id = tweet_id
            )
    else:
        response = "%s Can't find a rating for %s." % (username, movie)
        T.update_status(status = response)

def tweet_weather(regex, tweet, tweet_id, username):
    """Replies with the weather report"""

    location = re.sub(regex, '', tweet)
    report = get_weather(location)

    location_name, current, max_today, summary = report

    info = (
        username,
        location_name,
        current,
        max_today,
        summary
        )

    response = u"%s %s\nNow: %.0f\u2103 Max: %.0f\u2103\n%s" % info

    T.update_status(
        status = response,
        in_reply_to_status_id = tweet_id
        )

def tweet_link(tweet_id, username, link):
    """Replies with a link"""

    response = "%s %s" % (username, link)

    T.update_status(
        status = response,
        in_reply_to_status_id = tweet_id
        )

def tweet_this(message):
    """Will tweet out the given message"""
    T.update_status(status = message)
