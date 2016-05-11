import json

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

    # api.update_profile_colors(profile_sidebar_border_color=temp_colour)
    api.update_profile(name=name)


def main(config):
    weather = get_weather(config['forecast'])

    weather_emoji = ICON_TO_EMOJI.get(weather.icon, '')

    twitter_name = emoji.emojize('{1} {0}'.format(config['twitter']['name'],
                                 weather_emoji), use_aliases=True)

    data = TEMPERATURE_TO_COLOUR
    temp_colour = data.get(weather.temperature, data[min(data.keys(),
                           key=lambda k: abs(k-weather.temperature))])

    update_twitter_profile(twitter_name, temp_colour, config['twitter'])


if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.loads(f.read())

    main(config)
