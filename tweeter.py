#!/usr/bin/env python3

import time, tweepy, json, datetime

cfg = { 
    "consumer_key"        : "ADeBhHXYOgoNXgagWe7ZjRB3C",
    "consumer_secret"     : "dXzWSyFeFCAzgT7b9llIbG4nQ0YTN69BPnEfR7L9QlGPV4Pjfr",
    "access_token"        : "991703272636452865-QiM7NZWdo3kMxxmjW3ogkKSGhXGFu5S",
    "access_token_secret" : "UR7tgzgexIqFFajQw0pSdfZzSXehH4bntauWyzaQ6Wgkm"
}

auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
twitter = tweepy.API(auth)
myID = "991703272636452865"
tweet = "This is a test tweet: http://adambretsch.com"

#print(tweet)
#status = twitter.update_status(status=tweet)

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        name = data["user"]["name"]
        text = data["text"]
        userID = data["user"]["id"]
        print("Tweet: ",text)
        print("Name ",name)
	
        if ("Be my friend" == text):
           twitter.create_friendship(userID)
           message = "Welcome to the friendzone " + name
           twitter.send_direct_message(user_id=userID, text=message)
           print(name, " is now a friend")
        elif ("#IoTCoffee please" == text):
           if (twitter.get_user(userID).following):
              timedone = datetime.datetime.now() + datetime.timedelta(minutes=15)
              message = "Making you coffee now, will be done at " + str(timedone)
              twitter.send_direct_message(user_id=userID, text=message)
              print("Make the Coffee!")

    def on_error(self, status_code):
        if status_code == 420:
            return False

print("Starting tweet listener at ", datetime.datetime.now())
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = twitter.auth, listener=myStreamListener)

myStream.filter(track=['#IoTCoffee'])

