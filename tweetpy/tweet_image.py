
"""
Uses twitter endpoint to upload a picture
"""

import sys
import os
import urllib
import json
import base64
import requests

import oauth2 as oauth
from tweetpy.tweetpy import OAuthClient as OAuthClient
import tweetpy.tweet as tweet


class Tweet_Image():
    def __init__(self, img_path, status):
        self.url = 'https://upload.twitter.com/1.1/media/upload.json'
        self.image_path=''
        self.base64_image=None
        self.image_file=None
        self.status = ''
        self.image_path = img_path
        self.status = status
        self.image_size=0
        
    def read_image(self):
        self.image_size = os.path.getsize(self.image_path)
        with open(self.image_path, 'rb') as image_file:
            self.base64_image = base64.b64encode(image_file.read())
            self.image_file = image_file.read()
            
            
    
    def upload(self):
        consumer_key, consumer_secret, oauth_secret, oauth_token_secret = tweet.get_config_parameters()
        print (consumer_key, consumer_secret, oauth_secret, oauth_token_secret)
        oauthc = OAuthClient(consumer_key, consumer_secret)
        new_token = oauth.Token(oauth_secret, oauth_token_secret)
        client = oauth.Client(oauthc.consumer, new_token)
        
        #requests.post(self.url, files=self.image_file, auth=clien)
        
        initbody = 'media={}'.format(self.image_file)
        
        response = client.request(self.url, body=initbody, method='POST')
        print (response)
        
        #media_id = json.loads(response[1].decode('utf-8'))['media_id_string']
        
        
  #      
   #     appendbody = 'command=APPEND&media_id={}&segment_index=0'.format(media_id)
    #    response = client.request(self.url, body=appendbody, method='POST')
     #   
      #  endbody = 'command=FINALIZE&media_id={}'.format(media_id)
       # response = client.request(self.url, body=endbody, method='POST')
        return media_id
        
def upload_image(image_path, text):
    tup = Tweet_Image(image_path, text)
    tup.read_image()
    media_id = tup.upload()
    tweet.send_tweet(text, media=media_id)