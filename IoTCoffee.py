#!/usr/bin/env python3

import time, tweepy, json, datetime
import Adafruit_BBIO.GPIO as GPIO
import rcpy.servo as servo
import rcpy.motor as motor

ON ="GP0_6"  # GP0 for relays
OFF ="GP0_5"
WET ="P9_23"  # GP0 for buttons
UP = 0.7
DOWN = -0.9

servo1 = servo.servo1
pump = motor.motor3

servo.enable()
clk= servo1.start(0.02)
servo1.pulse(UP)
time.sleep(1)
servo.disable()
pump.set(0)

# Set the GPIO pins:
GPIO.setup(WET, GPIO.IN)
GPIO.setup(ON, GPIO.OUT)
GPIO.setup(OFF, GPIO.OUT)

GPIO.output(ON, 0)
GPIO.output(OFF, 0)

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

def makeCoffee():
  print("Begin makeCoffee()")
  
  print("lowering water arm")
  servo.enable()
  servo1.pulse(DOWN)
  time.sleep(2)
  servo.disable()
  
  while not GPIO.input(WET):
    print("no water found, pumping") 
    pump.set(1)
    time.sleep(0.5)
  print("water found!")
  pump.set(0)
  
  print("starting coffee maker")
  GPIO.output(ON, 1)
  time.sleep(1)
  GPIO.output(ON,0)
  
  time.sleep(5)

  #print("turn off coffee maker")
  #GPIO.output(OFF, 1)
  #time.sleep(1)
  #GPIO.output(OFF,0)

  #print("raising water arm")
  #servo1.pulse(UP)
  #time.sleep(1)


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
              makeCoffee()
              message = "Coffee is done at " + str(datetime.datetime.now())
              twitter.send_direct_message(user_id=userID, text=message)
           else:
             print("Cannot make coffee, user not followed")

    def on_error(self, status_code):
        if status_code == 420:
            return False

print("Starting tweet listener at ", datetime.datetime.now())
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = twitter.auth, listener=myStreamListener)

myStream.filter(track=['#IoTCoffee'])

