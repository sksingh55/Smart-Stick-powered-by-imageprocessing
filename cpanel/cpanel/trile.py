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



tz= pytz.timezone('Asia/Kolkata')
time_now= datetime.now(timezone.utc).astimezone(tz)
millis = int(time.mktime(time_now.timetuple()))
firebase = firebase.FirebaseApplication('https://cpanel-9935b.firebaseio.com/', None)


data = {
	"langitude":70.22,
	"latitude":555,
	}
url = '/users/' + str(millis) + '/'

try:
	firebase.post(url, data)
except:
	print("something went wrong")


users = database.child('users').get().val()
user = list(users)
data = database.child('users').child(user[-1]).get().val()
data = list(data)
location = database.child('users').child(user[-1]).child(data[0]).get().val()
location = list(location)


print(location)


