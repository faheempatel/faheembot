from forecastio import Forecastio
import datetime

forecast = Forecastio("89cf536aeaf4e0a4242b9dbea5fd4d03")

lat = 51.500152
lon = -0.126236

result = forecast.loadForecast(lat, lon, time=datetime.datetime.now(), units="si")
byHour = forecast.getHourly()
byDay = forecast.getDaily()

weather = [[hour.temperature, day.summary] for hour, day in zip(byHour.data, byDay.data)]
today = [[day.temperatureMin, day.temperatureMax, day.summary] for day in byDay.data]

current_temp = weather[0][0]
day_summary = weather[0][1]

print "Current Temp: %s \nDay Summary: %s" % (current_temp, day_summary)

min_today = round(today[0][0])
max_today = round(today[0][1])
summary_today = today[0][2]

print "Max: %s \nSummary: %s" % (int(min_today), int(max_today), summary_today)
