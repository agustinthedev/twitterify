import tweepy, sys, time

# Get Twitter connection string
def getTwitterConnectionString():
    with open("config/twitter.txt", "r") as file:
        return file.read().split(",")

try:
    # Get arguments
    args = sys.argv[1:]

    tweet_id = args[0]
    delay = args[1]
    connection_string = args[2].split(",")

    time.sleep(float(delay) * 60)

    # Connect to Twitter account

    client = tweepy.Client(
        consumer_key=connection_string[0], consumer_secret=connection_string[1],
        access_token=connection_string[2], access_token_secret=connection_string[3], wait_on_rate_limit=True
    )

    # Retweet tweet
    client.retweet(tweet_id=tweet_id)

    # Sleep for 8 hours
    time.sleep(8 * 60 * 60)

    # Unretweet
    client.unretweet(source_tweet_id=tweet_id)
except Exception as e:
    print(e)

