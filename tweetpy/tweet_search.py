"""
Uses twitter endpoint to search for a specific word
"""

import sys
import urllib
import json

import oauth2 as oauth
from tweetpy.tweetpy import OAuthClient as OAuthClient
import tweetpy.tweet as tweet

class TweetSearch():
    """
    Uses twitter search api
    """

    def __init__(self):
        self.__url = 'https://api.twitter.com/1.1/search/tweets.json?'
        self.__query = ''

    def build_query(self, query, recent, is_user):
        """
        Build query block for the url
        """
        query = self.__url + 'q=' + urllib.parse.quote(query, safe='')
        if recent:
            query += '&result_type=recent'
        if is_user:
            query += '&f=users'
        self.__query = query

    def search(self):
        """
        Uses oauth to search using the self._query as parameter
        """
        consumer_key, consumer_secret, oauth_secret, oauth_token_secret = tweet.get_config_parameters()

        oauthc = OAuthClient(consumer_key, consumer_secret)
        new_token = oauth.Token(oauth_secret, oauth_token_secret)
        client = oauth.Client(oauthc.consumer, new_token)
        response = client.request(self.__query, method='GET')

        json_dict = json.loads(response[1].decode())
        statuses = json_dict['statuses']
        for status in statuses:
            print("User: {} said: {} at: {}".format(status['user']['screen_name'],
                                                    status['text'],
                                                    status['created_at']))
            print('=' * 80)



def search(param):
    """
    Search the twitter api for sys.argv[1]
    """
    tweetSearch = TweetSearch()
    tweetSearch.build_query(param, True, False)
    tweetSearch.search()

