import os, tweepy, openai, random, re
import os.path
from sys import platform
from time import sleep
from datetime import datetime
from threading import Thread

#
# Main functions
#

class Core:

    def __init__(self):
        self.__createFolders()

    # Create neccesary folders
    def __createFolders(self):
        tweetsFolder = True if os.path.exists("assets/tweets/") else False
        configFolder = True if os.path.exists("assets/config/") else False

        if tweetsFolder is False: os.mkdir("assets/tweets/")
        if configFolder is False: os.mkdir("assets/config/")

    # Log message to console and save to log file
    def log(self, message):
        print(message)

    # Detect if Twitter credentials file exists
    def credentialsFileExists(self):
        credentialsFile = True if os.path.exists("assets/config/twitter.txt") else False
        return credentialsFile

    # Get Twitter bearer token
    def getTwitterBearerToken(self):
        with open("assets/config/bearer.txt", "r") as file:
            return file.read()

    # Get Twitter connection string
    def getTwitterConnectionString(self):
        with open("assets/config/twitter.txt", "r") as file:
            return file.read().split(",")

    # Get Twitter connection string RAW
    def getRAWTwitterConnectionString(self):
        with open("assets/config/twitter.txt", "r") as file:
            return file.read()

    # Save Twitter connection string to config file
    def saveTwitterCredentials(self, api_key, api_secret, access_token, access_token_secret, bearer_token):
        with open("assets/config/twitter.txt", "w") as file:
            connection_string = api_key + "," + api_secret + "," + access_token + "," + access_token_secret
            file.write(connection_string)

        with open("assets/config/bearer.txt", "w") as file:
            file.write(bearer_token)

    # Clear screen
    def clearScreen(self):
        os.system("cls") if platform == "win32" else os.system("clear")

    # Check if string contains URL
    def containsURL(self, text):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex, text)

        return False if len(url) == 0 else True

    # Calculate and return a chance
    def calculateChance(self, chance):
        generated_number = random.randint(1, 100)
        if generated_number <= chance:
            return True
        else:
            return False

    # Create file to add accounts followed
    def createFollowedFile(self):
        followedFile = os.path.exists("assets/followed.txt")

        if followedFile is False:
            f = open("assets/followed.txt", "a+")
            f.close()

    # Add username to followed list text file
    def addFollowed(self, username):
        with open("assets/followed.txt", "a") as file:
            file.write(username + ",")

    # Get the lsit of people already followed
    def getFollowed(self):
        with open("assets/followed.txt", "r+") as file:
            content = file.read()

        return content.split(",")

    # Get user Operative System
    def getUserOS(self):
        return "Windows" if platform == "win32" else "Linux"

    # Add specified tweet to auto retweet queue
    def getAutoRetweetCommand(self, tweet_id, delay, connection_string):
        os = self.getUserOS()

        if os == "Windows":
            command = "python assets/retweet.pyw " + str(tweet_id) + " " + str(delay) + " " + str(connection_string)
        else:
            command = "python3 assets/retweet.pyw " + str(tweet_id) + " " + str(delay) + " " + str(connection_string)

        return command

    # Check if txt file with accounts followed exists
    def followsFileExists(self):
        followsFile = True if os.path.isfile("assets/followed.txt") else False
        return followsFile


#
# Set up
#

def setUp():
    framework.clearScreen()
    framework.log("######### Set Up #########")
    framework.log(" ")

    api_key = input("→ Api Key: ")
    api_secret = input("→ Api Secret: ")
    access_token = input("→ Access Token: ")
    access_token_secret = input("→ Access Token Secret: ")
    bearer_token = input("→ Bearer Token: ")

    framework.saveTwitterCredentials(api_key, api_secret, access_token, access_token_secret, bearer_token)

    showMenu(False)


#
# Tweet Scraper
#

def tweetScraper():
    framework.clearScreen()

    # Tweepy connection to Twitter account
    token = framework.getTwitterBearerToken()
    client = tweepy.Client(token, wait_on_rate_limit=True)

    framework.log(" ")
    framework.log("######### Tweet Scraper #########")
    framework.log(" ")

    user_list_raw = input("→ Enter the usernames of the accounts you want to scrape tweets from, separated by a comma: ")
    user_list = user_list_raw.replace(" ", "").split(",")

    exclude_tweets_with_urls = input("→ Exclude tweets that contain URLs? (Y/N): ")

    if exclude_tweets_with_urls == "y" or exclude_tweets_with_urls == "Y":
        exclude_tweets_with_urls = True
    else:
        exclude_tweets_with_urls = False


    for user in user_list:

        try:
            # Get tweets from the user
            user_id = client.get_user(username=user).data.id
            tweets = client.get_users_tweets(id=user_id, max_results=100, exclude=["retweets", "replies"])

            for tweet in tweets.data:

                # Return if user selected to exclude tweets with URLs and tweet contains URLs
                if exclude_tweets_with_urls and framework.containsURL(tweet.text):
                    continue

                framework.clearScreen()

                tweets_amount = (len(list(os.walk('assets/tweets/'))) - 1)

                framework.log(" ")
                framework.log("######### Tweet Scraper #########")
                framework.log(" ")
                framework.log("(!) Selected accounts: " + user_list_raw)
                framework.log("(!) Amount of saved tweets: " + str(tweets_amount))
                framework.log("(!) Getting tweets from " + str(user))
                framework.log(" ")

                # Tweet ID
                tweet_id = tweet.id

                # Tweet full text
                tweet_text = tweet.text

                # Replace symbols

                tweet_text = tweet_text.replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

                # Present the tweets in screen
                framework.log("===============================================")
                framework.log(" ")
                framework.log(tweet_text)
                framework.log(" ")
                framework.log("===============================================")
                framework.log(" ")
                option = input("→ Type Y to save or press Enter to skip: ")

                # Check if user wants to save the tweet
                if option == "y" or option == "Y":
                    folder_path = "assets/tweets/" + str(tweet_id) + "/"
                    file_path = folder_path + "tweet.txt"

                    # Create tweet folder if it doesn't exist
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)

                    # Save tweet text to file
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(tweet_text)

                framework.clearScreen()
        except Exception as e:
            framework.log("ATTENTION: Error occurred with user " + str(user) + ", skipping to next user (if available).")
            print(str(e))
            sleep(10)

#
# Send Tweets
#


def writeVariation(text):
    prompt_text = "Rewrite this sentence '%text%' but using different words."
    parsed_prompt_text = prompt_text.replace("%text%", text)

    # Send request to OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=parsed_prompt_text,
        max_tokens=80
    )

    # Parse response
    tweet_response = str(response.choices[0].text).strip()

    phrases = tweet_response.split(".")

    parsed_reply = ""
    for phrase in phrases:
        phrase = phrase.strip()
        parsed_reply += phrase + "\n\n"

    # Return parsed response
    return parsed_reply

def startTweeting(variation, delay, retryOnError, retweet_delay):
    # Tweepy connection to Twitter account
    connection_string = framework.getTwitterConnectionString()

    client = tweepy.Client(
        consumer_key=connection_string[0], consumer_secret=connection_string[1],
        access_token=connection_string[2], access_token_secret=connection_string[3], wait_on_rate_limit=True
    )

    # Select a random tweet from the tweets folder
    tweets_folder = "assets/tweets/"
    available_tweets = os.listdir(tweets_folder)
    selected_tweet = random.choice(available_tweets)

    # Get the text of the selected tweet
    tweet_file = tweets_folder + selected_tweet + "/tweet.txt"
    with open(tweet_file, "r", encoding="utf-8") as file:
        tweet_text = file.read()

    # If True, create a variation of the text
    if variation is True:
        tweet_text = writeVariation(tweet_text)

    now = datetime.now()
    date_sent = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"

    # Try to send the tweet
    try:

        tweet = client.create_tweet(text=tweet_text)
        tweet_id = tweet.data["id"]
        framework.log(date_sent + " A new tweet has been sent. (Identifier: " + selected_tweet + ")")


        if retweet_delay != 0:
            try:
                # Launch script to auto retweet in background
                command = framework.getAutoRetweetCommand(tweet_id, retweet_delay, framework.getRAWTwitterConnectionString())

                thread = Thread(target = lambda: os.system(command))
                thread.start()
            except Exception as e:
                print(date_sent + " " + str(e))

        # Wait specified delay and launch function again
        sleep(float(delay) * 60)
        startTweeting(variation, delay, retryOnError, retweet_delay)

    except Exception as e:
        if retryOnError:
            print(str(e))
            startTweeting(variation, delay, retryOnError, retweet_delay)
        else:
            print(date_sent + " " + str(e))
            sleep(float(delay) * 60)

def sendTweets():

    framework.clearScreen()
    framework.log("######### Send Tweets #########")
    # Initial configuration by the user
    write_variation = input("→ Use AI to tweet variations of the selected tweets? (Y/N): ")
    tweet_delay = input("→ Delay between tweets (in minutes): ")
    retry = input("→ Immediately retry if fails to tweet? (Y/N): ")
    retweet = float(input("→ After how many minutes retweet your own tweet? (0 to disable): "))

    if write_variation == "Y" or write_variation == "y":
        write_variation = True

        openai_key = input("→ Please enter your OpenAI api key: ")
        openai.api_key = openai_key

    #else:
        #openai.api_key = "empty"

    if retry == "Y" or retry == "y":
        retry = True

    # Start tweeting process
    startTweeting(write_variation, tweet_delay, retry, retweet)

#
# Auto Retweet
#


def autoRetweet():
    framework.clearScreen()
    framework.log(" ")
    framework.log("######### Auto Retweet #########")
    framework.log(" ")

    user_list_raw = input("→ Enter the usernames of the accounts you want to retweet, separated by a comma: ")
    delay = float(input("→ Enter the delay between retweets (in minutes): "))

    user_list = user_list_raw.replace(" ", "").split(",")

    print(" ")

    connection_string = framework.getTwitterConnectionString()
    client = tweepy.Client(consumer_key=connection_string[0], consumer_secret=connection_string[1],
                           access_token=connection_string[2], access_token_secret=connection_string[3],
                           wait_on_rate_limit=True)

    # Turn usernames into ids

    user_ids = []
    for user in user_list:
        try:
            id = client.get_user(username=user, user_auth=True).data.id
            user_ids.append(id)

        except Exception as e:
            framework.log("- ERROR while trying to fetch " + user + ", skipping.")

    # Select random account, get tweets, filter and retweet
    already_retweeted = []
    while True:
        selected_account = random.choice(user_ids)

        try:
            tweets = client.get_users_tweets(id=selected_account, exclude=["retweets", "replies"],
                                             expansions=["author_id", "in_reply_to_user_id"], max_results=100,
                                             user_auth=True)

            for tweet in tweets.data:
                tweet_id = tweet.id
                tweet_text = tweet.text

                if tweet.in_reply_to_user_id is None and framework.containsURL(tweet_text) is False:
                    if tweet_id not in already_retweeted and int(tweet.author_id) == int(selected_account):
                        client.retweet(tweet_id=tweet_id)

                        now = datetime.now()
                        date_sent = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"
                        username = client.get_user(id=selected_account, user_auth=True).data.username

                        print(date_sent + " New retweet sent (Account: " + username + ")")

                        already_retweeted.append(tweet_id)

                        break

        except Exception as e:
            print(e)

        sleep(delay * 60)

#
# Auto Follow
#

def autoFollow():
    framework.clearScreen()
    framework.log(" ")
    framework.log("######### Auto Follow #########")
    framework.log(" ")

    # Tweepy connection to Twitter account

    connection_string = framework.getTwitterConnectionString()
    client = tweepy.Client(
        consumer_key=connection_string[0], consumer_secret=connection_string[1],
        access_token=connection_string[2], access_token_secret=connection_string[3],
        wait_on_rate_limit=True
    )

    delay = float(input("→ Enter the delay between follows (in minutes): "))
    tweets_raw = input("→ Enter the ID of the tweets you want to follow users from: ")
    unfollow_amount = int(input("→ After how many follows start unfollowing?: "))

    accounts_list = tweets_raw.replace(" ", "").split(",")
    followed_this_session = 0

    framework.clearScreen()
    framework.log(" ")
    framework.log("######### Auto Follow #########")
    framework.log(" ")
    framework.log("→ Selected tweets: " + tweets_raw)
    framework.log(" ")

    framework.createFollowedFile()

    for tweet in accounts_list:
        framework.log(" ")
        framework.log("(!) Getting and following " + str(tweet) + "'s likers.")
        framework.log(" ")

        paginator = tweepy.Paginator(client.get_liking_users, tweet, max_results=100, limit=20, user_auth=True)

        try:
            for page in paginator:
                for user in page.data:
                    username = user.username
                    user_id = client.get_user(username=username, user_auth=True).data.id

                    now = datetime.now()
                    date_sent = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"

                    framework.createFollowedFile()

                    if username in framework.getFollowed():
                        framework.log(date_sent + " Already tried following " + username + ", skipping.")

                        sleep(5)
                    else:
                        try:
                            client.follow_user(target_user_id=user_id)

                            followed_this_session += 1

                            framework.addFollowed(username)

                            framework.log(date_sent + " - Followed " + username + " - Total followed: " + str(
                                followed_this_session) + " - Next delay: " + str(delay) + " minutes")

                            # Check if should start auto unfollowing
                            if followed_this_session % unfollow_amount == 0:
                                launchAutoUnfollow(delay)

                            sleep(delay * 60)
                        except Exception as e:
                            framework.log(date_sent + " - ERROR - " + str(e))
        except Exception as e:
            framework.log(" (!) ERROR - " + str(e))

#
# Auto Unfollow
#

def autoUnfollow(delay):
    now = datetime.now()
    started_date = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"

    if os.path.isfile("assets/followed.txt"):
        try:
            # Rename the file
            file_new_name = now.strftime("%d-%m-%Y %H-%M-%S")
            file_new_path = "assets/" + file_new_name + ".txt"

            os.rename("assets/followed.txt", file_new_path)

            # Get all accounts followed
            with open(file_new_path, "r") as follows_file:
                accounts_followed = follows_file.read().split(",")

            # Delete empty spaces in list
            while ("" in accounts_followed):
                accounts_followed.remove("")

            # Connect to Twitter
            connection_string = framework.getTwitterConnectionString()
            client = tweepy.Client(
                consumer_key=connection_string[0], consumer_secret=connection_string[1],
                access_token=connection_string[2], access_token_secret=connection_string[3],
                wait_on_rate_limit=True
            )

            # Basic data
            accounts_total = len(accounts_followed)
            already_unfollowed = 0

            # Start unfollowing
            for user in accounts_followed:
                try:
                    user_id = client.get_user(username=user, user_auth=True).data.id
                    client.unfollow_user(target_user_id=user_id)

                    already_unfollowed += 1

                    now = datetime.now()
                    current_date = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"

                    framework.log(current_date + " - Unfollowed " + user + " - (" + str(already_unfollowed) + "/" + str(
                        accounts_total) + ") - Next delay: " + str(delay) + " minutes.")

                    sleep(delay * 60)

                except Exception as e:
                    already_unfollowed += 1

                    framework.log(started_date + " - Error while trying to unfollow " + user + ", skipping - (" + str(already_unfollowed) + "/" + str(accounts_total) + ")")

        except Exception as e:
            framework.log(started_date + " - ERROR: " + str(e))
    else:
        framework.log(started_date + " Follows file does not exist, stopping.")


def launchAutoUnfollow(delay):
    thread = Thread(target=autoUnfollow, args=[delay])
    thread.start()




#
# Interact
#

def writeReply(text):
    prompt = "Write a positive response to '%text%' using 280 characters maximum"

    parsed_prompt_text = prompt.replace("%text%", text)

    # Send request to OpenAI
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=parsed_prompt_text,
        max_tokens=90
    )

    reply = str(response.choices[0].text).strip()
    phrases = reply.split(".")

    parsed_reply = ""
    for phrase in phrases:
        phrase = phrase.strip()
        parsed_reply += phrase + "\n\n"

    # Return parsed response
    return parsed_reply

def checkForCharacters(text):
    forbidden_characters = [":", "↓", "🧵", "message me", "@"]
    usable = True

    for character in forbidden_characters:
        if character in text:
            usable = False

    return usable

def interact():
    framework.clearScreen()
    framework.log(" ")
    framework.log("######### Auto Interact #########")

    accounts_list = input("→ Enter the usernames of the accounts you want to reply to, separated by a comma: ")
    chance = int(input("→ Enter the chance of replying when the desired accounts tweet, from 0 (0%) to 100 (100%): "))
    open_ai_key = input("→ Enter your OpenAI key: ")

    accounts_list = accounts_list.replace(" ", "").split(",")
    openai.api_key = open_ai_key

    framework.log(" ")
    framework.log("######### Auto Interact #########")
    framework.log(" ")
    framework.log("Waiting for new tweets to interact with.")
    framework.log("Accounts: " + str(accounts_list))
    framework.log(" ")

    connection_string = framework.getTwitterConnectionString()
    client = tweepy.Client(consumer_key=connection_string[0], consumer_secret=connection_string[1],access_token=connection_string[2], access_token_secret=connection_string[3], wait_on_rate_limit=True)

    # Start Tweet Listener
    class TweetHandler(tweepy.StreamingClient):
        def on_tweet(self, tweet):
            now = datetime.now()
            date_sent = "[" + now.strftime("%d/%m/%Y %H:%M:%S") + "]"

            try:
                calculated_chance = framework.calculateChance(chance)
                if calculated_chance:
                    if tweet.in_reply_to_user_id is None and framework.containsURL(tweet.text) is False:
                        if checkForCharacters(tweet.text):
                            reply = str(writeReply(tweet.text)).replace(".", "\n\n")
                            tweet_id = tweet.id

                            try:
                                sleep(60)
                                client.create_tweet(text=reply, in_reply_to_tweet_id=tweet_id)

                                framework.log(date_sent + " Replied to a new tweet - Reference: " + str(tweet_id))
                            except Exception as e:
                                print(date_sent + " - ERROR - " + str(e))


            except Exception as e:
                print(date_sent + " - ERROR - " + str(e))
                sleep(60 * 5)

        def on_errors(self, errors):
            framework.log("- ERROR - " + str(errors))

        def on_timeout(self):
            framework.log("- TIMEOUT -")

    streaming = TweetHandler(framework.getTwitterBearerToken())

    # Delete all previous rules
    try:
        rules = streaming.get_rules().data
        if rules is None:
            pass
        else:
            for rule in rules:
                streaming.delete_rules(rule.id)
    except Exception as e:
        framework.log("- ERROR RULES - " + str(e))

    # Add rules to listener
    user_count = len(accounts_list)
    loop_count = 1

    rules_string = ""

    for user in accounts_list:
        if loop_count == user_count:
            rules_string += "from:" + user + " "
        else:
            rules_string += "from:" + user + " OR "

        loop_count += 1

    rules_string += "-is:retweet"
    #framework.log(" RULES STRING: " + rules_string)

    try:
        streaming.add_rules(tweepy.StreamRule(rules_string))
    except Exception as e:
        framework.log(" - RULES ADD ERROR - " + str(e))

    # Start filtering
    streaming.filter(expansions=["author_id", "in_reply_to_user_id"])




# Menu

framework = Core()

def showMenu(error):
    framework.clearScreen()

    if error:
        framework.log(" ")
        framework.log("ATTENTION: An error occurred, please try again.")

    framework.log(" ")
    framework.log("##################### Twitterify 0.3 #####################")
    framework.log(" ")
    framework.log("→ (0) Set up")
    framework.log("→ (1) Tweet Scraper")
    framework.log("→ (2) Send Tweets")
    framework.log("→ (3) Auto Retweet")
    framework.log("→ (4) Auto Follow")
    framework.log("→ (5) Interact")
    framework.log(" ")
    framework.log("############################################################")
    framework.log(" ")
    framework.log("Please enter an option:")

    try:
        option = int(input("→ "))

        if option == 0:
            # Set up
            setUp()

        elif option == 1:
            # Tweet Scraper
            tweetScraper()

        elif option == 2:
            # Send Tweets
            sendTweets()

        elif option == 3:
            # Auto Retweet
            autoRetweet()

        elif option == 4:
            # Auto Follow
            autoFollow()

        elif option == 5:
            # Interact
            interact()

    except Exception as e:
        #showMenu(True)
        print(e)

showMenu(False)

framework.log(" ")
input("· Activity finalized, press enter to close...")