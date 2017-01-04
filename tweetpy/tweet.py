
"""
Main twitter module
"""

import sys
import json
from tweetpy.tweetpy import OAuthClient as OAuthClient
from configparser import SafeConfigParser, NoSectionError, NoOptionError, ConfigParser




def read_config(config_file):
    """
        read configuration file for twitter credentials
    """
    parser = SafeConfigParser()
    parser.read(config_file)
    result = None
    try:
        access_token = parser.get('twitter_cred', 'access_token')
        access_token_secret = parser.get('twitter_cred', 'access_token_secret')
        result = (access_token, access_token_secret)
    except NoSectionError:
        return result
    except NoOptionError:
        return result
    return result

def get_config_parameters():
    """
    Opens and parse config.ini
    """
    config_file = './tweetpy/tweet.ini'
    consumer_key = 'qAO4SICbLvQFVG8gJKTVFK3nm'
    consumer_secret = 'X3k3epRHH1jOrmPuWz7BR6vkBHAPnUESb8dMgsg2coZ3qY5GwJ'
    config = read_config(config_file)

    if isinstance(config, tuple):
        oauth_secret = config[0]
        oauth_token_secret = config[1]
    else:
        print('Tokens not found')
        client = OAuthClient(consumer_key, consumer_secret)
        tokens = client.fetch_request_token()
        client.request_user_pin(tokens[b'oauth_token'].decode('utf-8'),
                                tokens[b'oauth_token_secret'].decode('utf-8'))
        response = client.fetch_access_token()
        oauth_secret = response[b'oauth_token'].decode('utf-8')
        oauth_token_secret = response[b'oauth_token_secret'].decode('utf-8')
        config = ConfigParser()
        config['twitter_cred'] = {'access_token' : oauth_secret,
                                  'access_token_secret' : oauth_token_secret}
        with open(config_file, 'w') as config_file_desc:
            config.write(config_file_desc)
    return [consumer_key, consumer_secret, oauth_secret, oauth_token_secret]


def send_tweet(tweet):
    """
        Gets argv[0] and post it as tweet for the authenticated user
        if no user available, go through the loggin proccess
    """

    consumer_key, consumer_secret, oauth_secret, oauth_token_secret = get_config_parameters()

    client = OAuthClient(consumer_key, consumer_secret)
    response = client.post_status(tweet, None, oauth_secret, oauth_token_secret)
    for resp in response:
        json_response = json.loads(resp.decode('utf-8'))
        formatted_response = "User: {} - said: {} - id: {}"
        print("")
        print(formatted_response.format(json_response['user']['screen_name'],
                                        json_response['text'],
                                        json_response['id_str']))
                                        