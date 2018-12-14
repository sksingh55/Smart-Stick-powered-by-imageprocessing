from time import sleep        
import RPi.GPIO as GPIO
from firebase import firebase
import time
from datetime import datetime, timezone
import pytz
import pyrebase


config = {
    'apiKey': "AIzaSyA78ED10LYHOJ8cGKxOSUSLW_opz5Dc3vQ",
    'authDomain': "cpanel-9935b.firebaseapp.com",
    'databaseURL': "https://cpanel-9935b.firebaseio.com",
    'projectId': "cpanel-9935b",
    'storageBucket': "cpanel-9935b.appspot.com",
    'messagingSenderId': "630776370716"
  }

rebase = pyrebase.initialize_app(config)

auth = rebase.auth()
database=rebase.database()

GPIO.setmode(GPIO.BOARD)
buttonPin =11

GPIO.setup( buttonPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(buttonPin) == True :
    	database.child("notification").set(0)
	