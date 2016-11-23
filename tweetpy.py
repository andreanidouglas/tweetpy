import urllib
import httplib2
import oauth2 as oauth

host = 'https://api.twitter.com/'
request_token = 'oauth/request_token'
authorize_token = 'oauth/authorize'
oauth_callback = 'oob'
consumer_key='IBlCOHn41nfVuNLdVhT2eG7mm'
consumer_secret='3Y4hbLpfIRbeTrXSsWXXhkGEP5KAboLVoQwVfhhY1EnwAad4Nt'
access_token = 'oauth/access_token'

class OAuthClient(httplib2.Http):
    def __init__(self, consumer_key, consumer_secret):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        self.client = oauth.Client(self.consumer)

    def fetch_request_token(self, **kwargs):
        self.method=oauth.SignatureMethod_HMAC_SHA1()
        req = oauth.Request.from_consumer_and_token(self.consumer, token=None, http_method="POST", http_url=host + request_token, parameters={'oauth_callback': oauth_callback}, body="", is_form_encoded=True)
        req.sign_request(self.method, self.consumer, None)
        scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(host+request_token)
        realm = urllib.parse.urlunparse((scheme, netloc, '', None, None, None))
        body = req.to_postdata()
        super(OAuthClient, self).__init__(**kwargs)
        content = httplib2.Http.request(self, host+request_token, method="POST", body=body, headers={'Content-Type': 'application/x-www-form-urlencoded', 'oauth_callback': 'oob'})
        return dict(urllib.parse.parse_qsl(content[1]))

    def request_user_pin(self, oauth_token, oauth_token_secret):
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        print("Please go to the following link:")
        print(host + authorize_token + '?oauth_token=' +  oauth_token)
        self.oauth_verifier = input("Enter PIN Number: ")

    def fetch_access_token(self):
        token = oauth.Token(self.oauth_token, self.oauth_token_secret)
        token.set_verifier(self.oauth_verifier)
        client = oauth.Client(self.consumer, token)

        resp, content = client.request(host + access_token, "POST")
        return dict(urllib.parse.parse_qsl(content))

    def verify_credentials(self, oauth_token, oauth_token_secret):
        verify_credentials = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        token = oauth.Token(oauth_token, oauth_token_secret)
        client = oauth.Client(self.consumer, token)
        response = client.request(verify_credentials, "GET")
        return response

    def post_status(self, status, oauth_token, oauth_token_secret):
        post_status = 'https://api.twitter.com/1.1/statuses/update.json'
        token = oauth.Token(oauth_token, oauth_token_secret)
        client = oauth.Client(self.consumer, token)
        response = client.request(post_status, body="status=" + status, method="POST")
        return response[1]


if __name__ == "__main__":
    twitter = OAuthClient(consumer_key, consumer_secret)
    token = twitter.fetch_request_token()
    twitter.request_user_pin(token[b'oauth_token'].decode('utf-8'), "")
    token_auth = twitter.fetch_access_token()
    print(token_auth)
    cred = twitter.verify_credentials(token_auth[b'oauth_token'].decode('utf-8'), token_auth[b'oauth_token_secret'].decode('utf-8'))
    #print(cred)

    #print(post_status, "Ola, Mundo!", token_auth[b'oauth_token'].decode('utf-8'), token_auth[b'oauth_token_secret'].decode('utf-8'))

