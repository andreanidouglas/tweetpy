import sys
import tweetpy.tweet as t

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
    
    t.send_tweet("This is a drill")
    
if __name__ == "__main__":
    main()