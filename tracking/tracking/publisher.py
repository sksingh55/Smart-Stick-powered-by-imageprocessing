import urllib2
import time
from datetime import datetime
import pytz
from firebase import firebase

_lat = 0.0
_log = 0.0
_acc = 0.0

def publishtoInternet(data):
    global _lat
    global _log
    global _acc
    _lat = "23.1801"
    _log =  "80.0269"
    _acc = data['accuracy']
    if()
    
    time_now= datetime.now()
    print(time_now)
    millis = int(time.mktime(time_now.timetuple()))
    firebas = firebase.FirebaseApplication('https://cpanel-9935b.firebaseio.com/', None)
    url = '/users/'+str(millis)+'/'
    try:
        firebas.post(url, data)
    except:
        print("something went wrong")
        log(data)

def log(temp):
    f = open('log','a')
    t = time.localtime(time.time())
    msg =str(t.tm_hour)+' ' + str(t.tm_min)
    f.write(msg)
    f.write('temp: ')
    f.write(temp)
    
    f.write('\n')
    f.close()
