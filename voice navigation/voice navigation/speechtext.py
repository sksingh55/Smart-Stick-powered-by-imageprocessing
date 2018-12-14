import speech_recognition as sr
import os
import direction
import textspeech
r=sr.Recognizer()
while (1):
	
	try:
	    with sr.Microphone() as source:
	            print("say something")
	            audio = r.listen(source)
	            print("time over")

	            x = (r.recognize_google(audio))
	            print(x)
	            if "detect" in x:
	                    print("run")
	                    os.system('python detection.py')
	                    print("done")
	            elif "direction" in x:
	                    textspeech.main("where you want to go")
	                    try:
	                    	r2=sr.Recognizer()
	                    	with sr.Microphone() as source2:
	                    		print("say something")
	                    		audio2 = r2.listen(source2)
	                    		print("time over")
	                    		x2=r2.recognize_google(audio2)
	                    		print(x2)
	                    		direction.main(x2)
	                    except :
	                    	textspeech.main("sorry we did not get you")
	except :
		continue

                    





