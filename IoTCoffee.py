#!/usr/bin/env python3

import time, tweepy, json, datetime
import Adafruit_BBIO.GPIO as GPIO
import rcpy.servo as servo
import rcpy.motor as motor

ON ="GP0_6"  # GP0 for relays
OFF ="GP0_5"
WET ="P9_23"  # GP0 for buttons

pump = motor.motor3
pump.set(0)

# Set the GPIO pins:
GPIO.setup(WET, GPIO.IN)
GPIO.setup(ON, GPIO.OUT)
GPIO.setup(OFF, GPIO.OUT)

GPIO.output(ON, 0)
GPIO.output(OFF, 0)

cfg = { 
    "consumer_key"        : "VDXOzIU8iMXAxOTGt7fiIZYX0",
    "consumer_secret"     : "PSkn6GnkqSo3ghZGw0mF4vvtYsEHgShqB24MLJZvre5BumLQFJ",
    "access_token"        : "991703272636452865-DAyKVHoOhGHsj6gjQTAEUAFdUWiJeDx",
    "access_token_secret" : "aFSF5ELQ7yRzRtANATVAuJTJqAGx3CXrTSKkj4wfQrHvU"
}

auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
twitter = tweepy.API(auth)
print("Authenticated", twitter.me().name)
myID = "991703272636452865"
tweet = "This is a test tweet: http://adambretsch.com"

#print(tweet)
#status = twitter.update_status(status=tweet)

def makeCoffee():
  print("Begin makeCoffee()")
  
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
  
  print("making coffee...")
  time.sleep(5*60)

  print("turn off coffee maker")
  GPIO.output(OFF, 1)
  time.sleep(1)
  GPIO.output(OFF,0)

def timeNow():
  return datetime.datetime.now() - datetime.timedelta(hours=4)

close = True
hot = False

class MyStreamListener(tweepy.StreamListener):

    def on_data(self, data):
        data = json.loads(data)
        #print(json.dumps(data, indent=4, sort_keys=True))
        text = ""
        try:
          if 'direct_message' in data.keys():
            text = data["direct_message"]["text"]
            userID = data["direct_message"]["sender_id"]
            #if 'sender' in data['direct_message'].keys():
              #name = data['sender']
              #print("Name ",name)
            print("Message: ",text)
        except ValueError:
          print("decoding json has failed")
	
        if ("Be my friend please" == text):
           twitter.create_friendship(userID)
           message = "Welcome to #IoTCoffee " #+ name
           twitter.send_direct_message(user_id=userID, text=message)
           print(name, " is now a friend")
        elif ("#IoTCoffee please" == text):
           if (twitter.get_user(userID).following):
              timedone = timeNow().now() + datetime.timedelta(minutes=5)
              message = "Making you coffee now, will be done at " + str(timedone)
              twitter.send_direct_message(user_id=userID, text=message)
              makeCoffee()
              message = "Coffee is done at " + str(timeNow().now())
              twitter.send_direct_message(user_id=userID, text=message)
        elif("#IoTCoffee in 30 minutes please"):
          if (twitter.get_user(userID).following):
             timedone = timeNow().now() + datetime.timedelta(minutes=30)
             message = "Making you coffee, will be done at " + str(timedone)
             twitter.send_direct_message(user_id=userID, text=message)
             print("waiting for 30 min delay")
             time.sleep(30*60)
             makeCoffee()
             message = "Coffee is done at " + str(timeNow().now())
             twitter.send_direct_message(user_id=userID, text=message)

           else:
             print("Cannot make coffee, user not followed")
           return close

    def on_error(self, status_code):
        if status_code == 420:
            return False

print("Starting tweet listener at ", TimeNow().now())
try:
  myStreamListener = MyStreamListener()
  myStream = tweepy.Stream(auth = twitter.auth, listener=myStreamListener)
  myStream.userstream()
  #myStream.filter(track=['#IoTCoffee'])
except KeyboardInterrupt:
  print("exiting IoTCoffee")
  close = False
  
