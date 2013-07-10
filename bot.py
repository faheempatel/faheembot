import re
import helpers
import config
from twython import TwythonStreamer

# TWITTER 
APP_KEY = config.CONSUMER_KEY
APP_SECRET = config.CONSUMER_SECRET
OAUTH_TOKEN = config.OAUTH_TOKEN
OAUTH_SECRET = config.OAUTH_SECRET

class MyStreamer(TwythonStreamer):

    def on_success(self, data):
        """Data Handler for the Twitter Stream"""

        if 'text' not in data:
            return

        movie_regex = r"@\w+ rate "
        weather_regex = r"@\w+ weather for "
        laugh_regex = r"@\w+ make me laugh"

        request = data['text'].lower()
        tweet_id = data['id']
        username = "@" + data["user"]["screen_name"]

        if re.match(movie_regex, request):
            helpers.tweet_rating(movie_regex, request, tweet_id, username) 

        elif re.match(weather_regex, request):
            helpers.tweet_weather(weather_regex, request, tweet_id, username)

        elif re.match(laugh_regex, request):
            link = helpers.make_me_laugh()
            helpers.tweet_link(tweet_id, username, link)

    def on_error(self, status_code, data):
        message = "@faheempatel Error: %s %s" % (status_code, data)
        helpers.tweet_this(message)
        self.disconnect()

stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_SECRET)    
stream.statuses.filter(track='@faheembot')
