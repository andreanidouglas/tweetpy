import sys
import tweetpy.tweet as t
import tweetpy.tweet_search as ts
import tweetpy.tweet_image as tup


import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("tweet", help="Tweet the given string")
    parser.add_argument("--search", help="Search the following string", action="store_true")
    parser.add_argument("--image", help="Upload the following image", action="store")
    
    
    args = parser.parse_args()
    
    if args.search:
        ts.search(args.tweet)
    elif args.image:
        tup.upload_image(args.image, args.tweet)
    else:
        t.send_tweet(args.tweet)
    
if __name__ == "__main__":
    main()