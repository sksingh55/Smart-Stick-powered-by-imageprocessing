from django.shortcuts import render
import pyrebase
from django.contrib.auth import logout
import time
from datetime import datetime, timezone
import pytz
from django.http import StreamingHttpResponse

config = {
    'apiKey': "AIzaSyA78ED10LYHOJ8cGKxOSUSLW_opz5Dc3vQ",
    'authDomain': "cpanel-9935b.firebaseapp.com",
    'databaseURL': "https://cpanel-9935b.firebaseio.com",
    'projectId': "cpanel-9935b",
    'storageBucket': "cpanel-9935b.appspot.com",
    'messagingSenderId': "630776370716"
  }

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
database=firebase.database()


def signIn(request):
    logged = 3
    try:
        x = database.child('users').get().val()
        print(x)
        logged = 0
    except:
        logged = 1
    print('sakdm-------------------')
    print(logged)

    context = {
        'signup_success': 0,
        'logged': logged
    }
    return render(request, "index.html", context)


def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")

    print("incoming")
    try:
        print("incoming")
        user = auth.sign_in_with_email_and_password(email,passw)

    except:
        message = "invalid cerediantials"
        return render(request,"index.html",{"msg":message, 'logged': 0})
    print(user['idToken'])
    request.session['uid']=str(user['idToken'])


    context = {
        "e":email,
        "logged": 0,
    }

    return render(request, "index.html",context)


def logoutt(request):
    logout(request)

    if request.user.is_authenticated:
        logged = 0
    else:
        logged = 1

    context = {
        'signup_success': 0,
        'logged': logged
    }
    return render(request,'index.html', context)


def signUp(request):
    return render(request,"signup.html")

def postsignup(request):

    if request.user.is_authenticated:
        logged = 0
    else:
        logged = 1

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    print("incomingpostsignup")
    user=auth.create_user_with_email_and_password(email,passw)
    uid = user['localId']
    data={"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)


    context = {
        'signup_success': 1,
        'logged': logged
    }

    return render(request,"index.html", context)


def create(request):

    return render(request,'create.html')


def post_create(request):
    tz= pytz.timezone('Asia/Kolkata')
    time_now= datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    work = request.POST.get('work')
    progress =request.POST.get('progress')
    url = request.POST.get('url')
    idtoken= request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
    "work":work,
    'progress':progress,
    'url':url
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})

def check(request):
    import datetime
    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users'][0]['localId']
    timestamps = database.child('users').child(a).child('reports').shallow().get().val()
    lis_time=list(timestamps)
    print(lis_time[-1])
    work = []

    for i in lis_time:

        wor=database.child('users').child(a).child('reports').child(i).child('work').get().val()
        work.append(wor)
    print(work)

    date=[]
    for i in lis_time:
        i = float(i)
        dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
        date.append(dat)

    print(date)

    comb_lis = zip(lis_time,date,work)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'check.html',{'comb_lis':comb_lis,'e':name})

def post_check(request):

    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    work =database.child('users').child(a).child('reports').child(time).child('work').get().val()
    progress =database.child('users').child(a).child('reports').child(time).child('progress').get().val()
    u =database.child('users').child(a).child('reports').child(time).child('url').get().val()
    print(u)
    i = float(time)
    dat = datetime.datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'post_check.html',{'w':work,'p':progress,'d':dat,'url':u,'e':name})



def track(request):
    print("run")
    import datetime
    idtoken = request.session['uid']
    a = auth.get_account_info(idtoken)
    a = a['users'][0]['localId']

    notification = database.child("notification").get().val()
    print(notification)

    print(a)
    timestamps = database.child('users').get().val()
    print(timestamps)
    lis_time=list(timestamps)
    print(lis_time[-1])
    id = list(database.child('users').child(lis_time[-1]).get().val())
    print(id)
    x = ((database.child('users').child(lis_time[-1]).child(id[0]).get().val()))

    return render(request,'check.html',{'longitude':x['longitude'],'latitude':x['latitude'], 'notification': notification})

def video(request):


    import io
    import picamera
    import logging
    import socketserver
    from threading import Condition
    import time
    from http import server

    PAGE="""\
    <html>
    <head>
    <title>Raspberry Pi - Surveillance Camera</title>
    </head>
    <body>
    <center><h1>Raspberry Pi - Surveillance Camera</h1></center>
    <center><img src="stream.mjpg" width="640" height="480"></center>
    <a href="http://192.168.43.208:8080/welcome.html">Close streaming</a>

    </body>
    </html>
    """

    class StreamingOutput(object):
        def __init__(self):
            self.frame = None
            self.buffer = io.BytesIO()
            self.condition = Condition()

        def write(self, buf):
            if buf.startswith(b'\xff\xd8'):
                self.buffer.truncate()
                with self.condition:
                    self.frame = self.buffer.getvalue()
                    self.condition.notify_all()
                self.buffer.seek(0)
            return self.buffer.write(buf)

    class StreamingHandler(server.BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                print(3)
                self.send_response(301)
                self.send_header('Location', '/index.html')
                self.end_headers()
            elif self.path == '/index.html':
                print(4)
                content = PAGE.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            elif self.path == '/stream.mjpg':
                print(43)
                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
                self.end_headers()
                try:
                    count = 0
                    while True:
                        count = count+1
                        print(count)
                        if(count>150):
                            camera.close()
                            break
                            
                            
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                        self.wfile.write(b'--FRAME\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b'\r\n')
                    print(1234)
                
                    
                except Exception as e:
                    print(3)
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
            else:
                print(4)
                self.send_error(404)
                self.end_headers()
            print(1223)
            
            print(12333)
        
        def finish(self):
            print("end")
            if not self.wfile.closed:
                self.wfile.flush()
                self.wfile.close()
                self.rfile.close()
                server.server_close()
                

    class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True

    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        print(camera)
    
        output = StreamingOutput()
        print(output)
        #Uncomment the next line to change your Pi's Camera rotation (in degrees)
        #camera.rotation = 90
        camera.start_recording(output, format='mjpeg')
        try:
            print(1)
            address = ('', 8000)
            x=0
            server = StreamingServer(address, StreamingHandler)
            print(server)
            if(server):
                print("sdcs")
            try:
                server.serve_forever()
                print("cdds")
                return render(request,'welcome.html')
            except KeyboardInterrupt:
                print('Stopping server')
        
        finally:
            print("vd")
            camera.stop_recording()
            return render(request,'welcome.html')
    return render(request,'welcome.html')
    

def home(request):
    return render(request,'welcome.html')
