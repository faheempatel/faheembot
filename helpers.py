import praw
import config
import datetime
from rottentomatoes import RT
from pygeocoder import Geocoder
from forecastio import Forecastio

# FORECAST.IO
forecast = Forecastio(config.F_KEY)

# ROTTEN TOMATOES
rt = RT(config.RT_KEY)

# REDDIT
r = praw.Reddit(user_agent="faheembot")

def rate(movie):
    """Given a movie title will return the Rotten Tomatoes score for it"""
    try: 
        json = rt.search(movie)[0]
        title = json['title'] 
        rating = json['ratings']['critics_score']
        return (title, rating)
    except IndexError:
        return ()

def make_me_laugh():
    """Returns the top r/funny link"""
    result = r.get_subreddit('funny').get_top(limit=1)
    top_post = result.next()
    return top_post.short_link

def weather(location):
    """Returns today's forecast for the given location"""

    # Find latitude and longitude values
    results = Geocoder.geocode(location)
    name_of_place_found = str(results[0])
    coordinates = results[0].coordinates
    lat, lon = coordinates

    # Get forecast
    forecast.load_forecast(
                            lat,
                            lon,
                            time=datetime.datetime.now(),
                            units="si"
                          )

    current = forecast.get_currently()
    byDay = forecast.get_daily()
    today = byDay.data[0]

    report = (
                 name_of_place_found,
                 current.temperature,
                 today.temperatureMax,
                 today.summary
             )

    return report
