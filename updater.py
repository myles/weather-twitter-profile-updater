import os
import json
from datetime import datetime

import emoji
import tweepy
import forecastio

# Colours came from <http://www.metoffice.gov.uk/guide/weather/symbols>.
TEMPERATURE_TO_COLOUR = {
    -30: 'FFFFFF', -28: 'F5F5F5', -26: 'EBEBEB', -24: 'E1E1E1', -22: 'BEBEBE',
    -20: '828282', -18: '545572', -16: '5D107B', -14: '59467C', -12: '2D107B',
    -10: '00107D', -8: '003BAE', -6: '002BF6', -4: '0083F8', -2: '00C0FA',
    0: '00FFFE', 2: '00F6C9', 4: '00D592', 6: '00A96A', 8: '00A83F',
    10: '00C646', 12: '00FC48', 14: 'C9FC4B', 16: 'FFFC4D', 18: 'F1EB8A',
    20: 'EBCA72', 22: 'E5AD57', 24: 'FFA934', 26: 'FF5520', 28: 'FF0A17',
    30: 'D7060F', 32: 'BA040C', 34: '9F0308', 36: '820205'
    }

ICON_TO_EMOJI = {
    'clear-day': ':sunny:',
    'clear-night': ':milky_way:',
    'rain': ':umbrella:',
    'snow': ':snowflake:',
    'sleet': '',  # TODO Figure out an appropriate emoji for sleet.
    'wind': ':dash:',
    'fog': ':foggy:',
    'partly-cloudy-day': ':partly_sunny:',
    'partly-cloudy-night': ''  # TODO Figure out an apporpriatea emoji.
    }

SPECIAL_DAYS_EMOJI = {
    '01-01': ':fireworks:',
    '03-20': ':tulip:',
    '06-21': ':surfer:',
    '09-19': ':birthday:',
    '09-22': ':fallen_leaf:',
    '10-31': ':ghost:',
    '12-21': ':snowman:',
    '12-25': ':santa:',
    '12-31': ':tada:',
    }


def get_weather(config):
    forecast = forecastio.load_forecast(config['api_key'], config['lat'],
                                        config['lng'])
    return forecast.currently()


def update_twitter_profile(name, temp_colour, config):
    auth = tweepy.OAuthHandler(config['consumer_key'],
                               config['consumer_secret'])
    auth.set_access_token(config['access_token'],
                          config['access_token_secret'])

    api = tweepy.API(auth)

    # This was disabled because for some reason it returns a 404 error.
    # api.update_profile_colors(profile_sidebar_border_color=temp_colour)

    api.update_profile(name=name)


def main(config):
    weather = get_weather(config['forecast'])
    weather_emoji = ICON_TO_EMOJI.get(weather.icon, '')

    today = datetime.now().strftime('%m-%d')
    special_day_emoji = SPECIAL_DAYS_EMOJI.get(today)

    if special_day_emoji:
        twitter_name = emoji.emojize('{0} {1} {2}'.format(weather_emoji,
                                                          'Myles',
                                                          special_day_emoji),
                                     use_aliases=True)
    else:
        twitter_name = emoji.emojize('{0} {1}'.format(weather_emoji,
                                                      'Myles Braithwaite'),
                                     use_aliases=True)

    data = TEMPERATURE_TO_COLOUR
    temp_colour = data.get(weather.temperature, data[min(data.keys(),
                           key=lambda k: abs(k-weather.temperature))])

    update_twitter_profile(twitter_name, temp_colour, config['twitter'])


if __name__ == "__main__":
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'config.json')

    with open(config_file, 'r') as f:
        config = json.loads(f.read())

    main(config)
