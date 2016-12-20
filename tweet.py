"""
Main twitter module
"""

import sys
import json
from tweetpy import OAuthClient
from configparser import SafeConfigParser, NoSectionError, NoOptionError, ConfigParser


config_file = 'tweet.ini'
consumer_key=''
consumer_secret=''

def read_config():
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

if __name__ == '__main__':
    TWITTER = OAuthClient(consumer_key, consumer_secret)
    config = read_config()
    if isinstance(config, tuple):
        oauth_secret = config[0]
        oauth_token_secret = config[1]
    else:
        print('Tokens not found')
        client = OAuthClient(consumer_key, consumer_secret)
        tokens = client.fetch_request_token()
        client.request_user_pin(tokens[b'oauth_token'].decode('utf-8'), tokens[b'oauth_token_secret'].decode('utf-8'))
        response = client.fetch_access_token()
        oauth_secret = response[b'oauth_token'].decode('utf-8')
        oauth_token_secret = response[b'oauth_token_secret'].decode('utf-8')
        config = ConfigParser()
        config['twitter_cred'] = {'access_token' : oauth_secret,
                                  'access_token_secret' : oauth_token_secret}
        with open(config_file, 'w') as config_file_desc:
            config.write(config_file_desc)
            
    client = OAuthClient(consumer_key, consumer_secret)
    response = client.post_status(sys.argv[1], None, oauth_secret, oauth_token_secret)
    for resp in response:
        json_response = json.loads(resp.decode('utf-8'))
        formatted_response = "User: {} - said: {} - id: {}"
        print(formatted_response.format(json_response['user']['screen_name'],
                                        json_response['text'],
                                        json_response['id_str']))
