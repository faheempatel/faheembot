import re
import helpers
import config
from twython import Twython, TwythonStreamer

# TWITTER 
OAUTH_TOKEN = config.OAUTH_TOKEN
OAUTH_SECRET = config.OAUTH_SECRET
CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET

t = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)    

movie_regex = "@\w+ rate "
weather_regex = "@\w+ weather for "
laugh_regex = "@\w+ make me laugh"

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
                    response = "%s %s is rated %s/100" % (username, title, rating)
                    t.update_status(status = response)
                else:
                    response = "%s Can't find a rating for %s." % (username, movie)
                    t.update_status(status = response)

            elif re.match(weather_regex, request):
                location = re.sub(weather_regex, '', request)
                report = helpers.weather(location)

                location_name, min_today, max_today, summary = report
                info = (username, location_name, min_today, max_today, summary)

                response = u"%s %s\nMin: %.0f\u2103 Max: %.0f\u2103\n%s" % info
                t.update_status(status = response)

            elif re.match(laugh_regex, request):
                link = helpers.make_me_laugh()
                response = "%s Oh you've gotta see this: %s" % (username, link)
                t.update_status(status = response)
        except KeyError:
            # FIX THIS
            print "Key error"

    def on_error(self, status_code):
        tweet = "@faheempatel Error: %s" % status_code
        t.update_status(status = tweet)
        print status_code

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)    
stream.user()
