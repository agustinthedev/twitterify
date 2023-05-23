import subprocess
from sys import platform

def checkOutputTweepy(output):
    if "Requirement already satisfied" in output:
        return True

    elif "Successfully installed tweepy" in output:
        return True

    else:
        return False
def checkOutputOpenAI(output):
    if "Requirement already satisfied" in output:
        return True

    elif "Successfully installed openai" in output:
        return True

    else:
        return False

# Get user platform
userOS = "Windows" if platform == "win32" else "Linux"

# Starting
print("########## Twitterify Installer ########## ")
print(" ")


# Install Tweepy
print("· Trying to install Tweepy...")

if userOS == "Windows":
    tweepy_result = subprocess.getoutput("pip install tweepy")
else:
    tweepy_result = subprocess.getoutput("python3 -m pip install tweepy")

output = checkOutputTweepy(tweepy_result)

if output:
    print("(!) Successfully installed Tweepy.")
else:
    print("(!) Could not install Tweepy correctly.")
    print("(!) Please try running the following command in the command line and send me a screenshot:")
    print("(!) Windows: pip install tweepy")
    print("(!) Linux/Mac Os: python3 -m pip install tweepy")


# Break
print(" ")
input("· Please press enter to continue...")
print(" ")


# Install OpenAI
print("· Trying to install OpenAI...")

if userOS == "Windows":
    tweepy_result = subprocess.getoutput("pip install openai")
else:
    tweepy_result = subprocess.getoutput("python3 -m pip install openai")

output = checkOutputOpenAI(tweepy_result)

if output:
    print("(!) Successfully installed OpenAI.")
else:
    print("(!) Could not install Tweepy correctly.")
    print("(!) Please try running the following command in the command line and send me a screenshot:")
    print("(!) Windows: pip install openai")
    print("(!) Linux/Mac Os: python3 -m pip install openai")


# Close
print(" ")
input("Installation finished, press enter to close...")