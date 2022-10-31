# Retrieve and print weather info for Merriam KS
# TODO:
# - Include sunrise/set info in output.
# - Add basic filtering for weather conditions
import json
from datetime import datetime
from time import time
from os.path import getmtime, exists
from subprocess import run

json_file = 'forecast.json'
wthr_url = 'https://api.openweathermap.org/data/2.5/forecast?lat=39.007380&lon=-94.723973&units=imperial&appid=60406d81d44b674d83ab9575e9db72f8'

if not exists(json_file) or (time() - getmtime(json_file)) > 3600:
    # Get a new forecast every hour
    run(['curl', '-o', json_file, wthr_url])

with open(json_file, encoding="utf-8") as f:
    wthr_json = json.load(f)

deg_bin = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
last_day = 0
for hr3 in wthr_json['list']:
    dt = datetime.fromtimestamp(hr3['dt'])
    if dt.day != last_day:
        print('\nDay  Time  Temp  Feel  Wind  Gust  Dir')
        last_day = dt.day
    deg = hr3['wind']['deg'] + 22.5
    if deg >= 360:
        deg -= 360
    deg_index = int(deg/45)
    print(dt.strftime('%a, %I %p'), '{temp:4.1f} ({feels_like:4.1f})'.format(**hr3['main']),
            '{speed:4.1f} ({gust:4.1f}) {deg:3d}'.format(**hr3['wind']),
            '{:2s}'.format(deg_bin[deg_index]), 
            '*'*int(hr3['wind']['speed']))

