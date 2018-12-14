import sys,time,track,publisher
from subprocess import call
SleepTime = 10 
_lat = 0.00
_lon = 0.00
_acc = 0.00

    
def maintain():
    print("2")
    global _lat
    global _lon
    global _acc
    (lat,lon,accuracy) = track.mainf()
    
    if(lat != _lat or lon !=_lon):
        data = {
                'longitude':lon,
                'latitude':lat,
                'accuracy':accuracy
                }
        print ("publishing ")
        print(data)
        publisher.publishtoInternet(data)
        _lat = lat
        _lon = lon
        _acc = accuracy
    else:
        print ("no change in coordinates")

print ("program begins")
while True:
    try:
        maintain()
    except Exception as inst:
        print (type(inst))
        print (' exception captured')
        print (inst)
        sys.stdout.flush()
    for i in range(0,SleepTime):
        sys.stdout.write("\restarting in %d seconds " % (SleepTime-i))
        sys.stdout.flush()
        time.sleep(1)





       
