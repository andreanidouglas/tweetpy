"""
Twitter OAuth API Handler.
"""

import httplib2
import oauth2 as oauth
import json
import urllib

host = 'https://api.twitter.com/'
request_token = 'oauth/request_token'
authorize_token = 'oauth/authorize'
oauth_callback = 'oob'
access_token = 'oauth/access_token'

class OAuthClient(httplib2.Http):
    """
    OAuth Client to negotiate twitter user login
    """

    def __init__(self, consumer_key, consumer_secret):
        super().__init__()
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.client = oauth.Client(self.consumer)
        self.__response = []
        self.method = None
        self.oauth_token = ""
        self.oauth_token_secret = ""
        self.oauth_verifier = ""

    def fetch_request_token(self, **kwargs):
        """
        Fetch initialization token from twitter. This will be used to complete the login process
        """

        self.method = oauth.SignatureMethod_HMAC_SHA1()

        req = oauth.Request.from_consumer_and_token(self.consumer,
                                                    token=None,
                                                    http_method="POST",
                                                    http_url=host + request_token,
                                                    parameters={'oauth_callback': oauth_callback},
                                                    body="",
                                                    is_form_encoded=True)


        req.sign_request(self.method, self.consumer, None)
        scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(host+request_token)
        urllib.parse.urlunparse((scheme, netloc, '', None, None, None))
        body = req.to_postdata()
        super(OAuthClient, self).__init__(**kwargs)
        content = httplib2.Http.request(self,
                                        host+request_token,
                                        method="POST",
                                        body=body,
                                        headers={'Content-Type':'application/x-www-form-urlencoded',
                                                 'oauth_callback': 'oob'})
        return dict(urllib.parse.parse_qsl(content[1]))

    def request_user_pin(self, oauth_token, oauth_token_secret):
        """
        Redirect user to the twitter login page to request the pin.

        The pin must be entered to the program
        """

        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        print("Please go to the following link:")
        print(host + authorize_token + '?oauth_token=' +  oauth_token)
        self.oauth_verifier = input("Enter PIN Number: ")

    def fetch_access_token(self):
        """
        Complete the login process with the assigned credentials from server
        """

        new_token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        new_token.set_verifier(self.oauth_verifier)
        client = oauth.Client(self.consumer, new_token)

        resp, content = client.request(host + access_token, "POST")
        
        return dict(urllib.parse.parse_qsl(content))

    def verify_credentials(self, oauth_token, oauth_token_secret):
        """
        Helper method to verify if assigned credentials are valid
        """

        self.__response = []
        verify_credentials = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        token = oauth.Token(oauth_token, oauth_token_secret)
        client = oauth.Client(self.consumer, token)
        response = client.request(verify_credentials, "GET")
        self.__response.insert(0, response)
        return self.__response


    def post_status(self, status, in_reply_to, oauth_token, oauth_token_secret, keep_last_response=False, media=None):
        """
        Create a twitter from the logged user
        """

        if not keep_last_response:
            self.__response = []
        post_status = 'https://api.twitter.com/1.1/statuses/update.json'
        if len(status) >= 140:
            response = self.post_multipart_status(status,
                                                  in_reply_to,
                                                  oauth_token,
                                                  oauth_token_secret)
            self.__response.append(response)
            return self.__response
        new_token = oauth.Token(oauth_token, oauth_token_secret)
        client = oauth.Client(self.consumer, new_token)
        
        if in_reply_to:
            body = "status={}&in_reply_to_status_id={}".format(status, in_reply_to)
        elif media != None:
            body = "status={}&media_ids={}".format(status, media)
        else:
            body = "status={}".format(status)
        
        print(body)
        response = client.request(post_status, body=body, method="POST")
        self.__response.insert(0, response[1])
        return self.__response

    def post_multipart_status(self, status, in_reply_to, oauth_token, oauth_token_secret):
        """
        Splice a post with more than 140 characters into multiple twittes.
        Link by the in_reply_to code
        """

        char = '0'
        char_pos = 137
        while char != ' ':
            char_pos -= 1
            char = status[char_pos]
            print(char_pos)

        new_status = status[0: int(char_pos)] + "..."

        response = self.post_status(new_status,
                                    in_reply_to,
                                    oauth_token,
                                    oauth_token_secret,
                                    True)[0]
        json_response = json.loads(response.decode('utf-8'))
        status_id = json_response['id_str']

        old_status = "@{} {}".format(json_response['user']['screen_name'],
                                     status[int(char_pos): len(status)])

        return self.post_status(old_status, status_id, oauth_token, oauth_token_secret, True)[0]
