#faheembot

##TODO
- Implement Twitter's streaming API
    - Seems to need two tweets per request... investigate.
        - Culprit: https://github.com/ryanmcgrath/twython/issues/202 
- <del>Add forecast.io support</del>
- Add reminder feature
- Implement nice fallbacks should the tweet length exceed 140 chars
    - For the weather build a URL to take you straight to forecast.io's site
- Add public transport features
    - Bus times
    - Tube line info
- Implement more rigorous parsing of incoming tweet
- <del>Keep conversation chain intact</del>
- Emoji for weather tweet?
- Add automated features
    - Weather report every morning
    - Tweet when tube lines are down
- Refactor!
