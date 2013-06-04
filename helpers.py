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
    json = rt.search(movie)[0]
    title = json['title'] 
    rating = json['ratings']['critics_score']
    return (title, rating)

def make_me_laugh():
    """Returns the top r/funny link"""
    result = r.get_subreddit('funny').get_top(limit=1)
    top_link = [str(post.short_link) for post in result][0]
    return top_link

def weather(location):
    """Returns today's forecast for the given location"""

    # Find longitude and latitude values
    results = Geocoder.geocode(location)
    found_location_name = results[0]
    coordinates = results[0].coordinates
    lon, lat = coordinates

    # Get forecast
    forecast.load_forecast(
                            lon,
                            lat,
                            time=datetime.datetime.now(),
                            units="si"
                          )

    byDay = forecast.get_daily()

    report = [(
                 str(found_location_name),
                 day.temperatureMin,
                 day.temperatureMax,
                 day.summary
              )
              for day in byDay.data
             ]

    # Return a flattened tuple
    return sum(report, ())
