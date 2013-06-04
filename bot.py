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
            username = str("@" + data["user"]["screen_name"])

            if re.match(movie_regex, request):
                movie = re.sub(movie_regex, '', request)
                title, rating = helpers.rate(movie)
                response = "%s %s is rated %s/100" % (username, title, rating)
                t.update_status(status = response)

            elif re.match(weather_regex, request):
                location = re.sub(weather_regex, '', request)
                report = helpers.weather(location)
                response = "%s\n %s Min: %s Max: %s\n%s" % (username, report[0], report[1], report[2], report[3])
                t.update_status(status = response)

            elif re.match(laugh_regex, request):
                link = helpers.make_me_laugh()
                response = "%s Oh you've gotta see this: %s" % (username, link)
                t.update_status(status = response)
        except KeyError:
            # FIX THIS
            print "Key error"

    def on_error(self, status_code):
        print status_code

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)    
stream.user()
