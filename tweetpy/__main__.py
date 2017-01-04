import sys
import tweetpy.tweet as t
import tweetpy.tweet_search as ts

import argparse

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("tweet", help="Tweet the given string")
    parser.add_argument("--search", help="Search the following string", action="store_true")
    
    args = parser.parse_args()
    
    if args.search:
        ts.search(args.tweet)
    
if __name__ == "__main__":
    main()