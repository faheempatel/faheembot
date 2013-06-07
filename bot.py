import re
import helpers
import config
from twython import Twython, TwythonStreamer

# TWITTER 
KEY = config.CONSUMER_KEY
SECRET = config.CONSUMER_SECRET
OAUTH_TOKEN = config.OAUTH_TOKEN
OAUTH_SECRET = config.OAUTH_SECRET

t = Twython(KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET)    

movie_regex = r"@\w+ rate "
weather_regex = r"@\w+ weather for "
laugh_regex = r"@\w+ make me laugh"

def tweet_rating(username, title, rating):
    response = "%s %s is rated %s/100" % (username, title, rating)
    t.update_status(status = response)

def tweet_weather(username, report):
    location_name, min_today, max_today, summary = report
    info = (username, location_name, min_today, max_today, summary)

    response = u"%s %s\nMin: %.0f\u2103 Max: %.0f\u2103\n%s" % info
    t.update_status(status = response)

def tweet_link(username, link):
    response = "%s %s" % (username, link)
    t.update_status(status = response)

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        try: 
            request = data['text'].lower()
            username = "@" + data["user"]["screen_name"]

            if re.match(movie_regex, request):
                movie = re.sub(movie_regex, '', request)
                result = helpers.rate(movie)
                if result:
                    title, rating = result
                    tweet_rating(username, title, rating)
                else:
                    response = "%s Can't find a rating for %s." % (username, movie)
                    t.update_status(status = response)

            elif re.match(weather_regex, request):
                location = re.sub(weather_regex, '', request)
                report = helpers.weather(location)
                tweet_weather(username, report)

            elif re.match(laugh_regex, request):
                link = helpers.make_me_laugh()
                tweet_link(username, link)
        except KeyError:
            # FIX THIS
            print "Key error"

    def on_error(self, status_code, data):
        tweet = "@faheempatel Error: %s" % status_code
        t.update_status(status = tweet)
        print status_code

stream = MyStreamer(KEY, SECRET, OAUTH_TOKEN, OAUTH_SECRET)    
stream.user()
