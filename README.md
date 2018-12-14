# Smart-Stick-powered-by-imageprocessing
As a part of design project . I design a stick which detects the object in front of it like car, stair etc and informs the blind person about the object and direct him to avoid it in real time. It has voice navigation feature. SOS notification which sends alert message to all the app users in range of 1 km. It also have security features like real time video surveillance and real time tracking

# Features Worked Upon:

# 1.Tracking stick:
# Objective : 
Real Time tracking of the user of the stick.

# Problem Solved: 
For an elderly or blind person its common to forget               
path and go in the wrong direction, so by real time 
tracking we can know the exact location of the person.
If the person needs help then we can also track his/her
exact location . 

# Equipments Used: 
Rasberry Pi 3
8 Gb memory Card
Card Reader
USB Dongle
Sim with data connection (BSNL)	
Power Bank as power source

# Technology Used:
Raberian OS
Geocoder API 
Python Programming Language


# Circuit :


The circuit has a camera connected to the raspberry pi for image detection.
The power to the circuit is given by standard power bank and the cable is seen connected to it in the image above.
The red wires in the circuit above are connected to the notification button. The user will press the button incase of any emergency.
The whole circuit is kept inside the plastic box to preserve it.


# Working:
Step 1: Power Supply



First thing we do is to give power to rasberry pi, for that we will use a standard power-bank.
We used 4G Dongle to connect it to the internet service.

Step 2: Get Location From Cell Tower/ Ip Address


First Step is to Get location of the moving Rasberry pi.
For the above we will scan the Ip address from the link below:
http://192.168.0.1/ 
By following the above steps we will get the location    
of the sim.

Step 3: Convert Location into coordinate and store into 	cloud
We will convert the location of the Sim and convert it into longitude and latitude using Geocoder (Google Api).
 We upload the Longitude and Latitude into the AWS cloud so that it can be used further .

# Code:
https://drive.google.com/drive/folders/19ge-Hxs7sn2udwdg4GvdNLcwjC_YLbYe?usp=sharing
	
	
	Run the code main.py by command sudo python
	main.py . 
	Main.py call two file track.py and publisher.py 
	Track.py scan the wifi or sim and get the 	address . We used           geocoder (google api ) to get 	the co-ordinates then return it to main.py . Then 	main.py call the publisher.py which upload the 	longitude and latitude to firebase .
Main.py continuing the above process after every 10 second.While tracking we extract the latest location and show on google map.
	




# 2. Emergency Notification:
# Objective:
Send a notification to all the users within 1 km when 
that  person needs help.
# Problem Solved:
If a user needs emergency help then its useless to send          
notification to an acquaintance who is miles away.
So,we are sending the notification to all the active
webapp users within a range of 5 km with the   
location so that   	the user can easily each .
Other technologies used:
Pusher (google cloud api for streaming notification)
Trigger Button

# Working:
Step 1: Trigger Button
When a person needs help then he would press a button on the handle . From the button we will get the co-ordinates of the stick (from sim location to latitude and longitude as in previous case).
Step 2: Sending Notification
Latitudes and Longitudes are send to the server with a help message as soon as new data come in server , data will be broadcasted .We have store the location of every new user in firebase . On button press we extract the location of all the user , create a circle of 1Km and send it to all the user.

# Code:
https://drive.google.com/drive/folders/16qG3ctxyNRwmRs9M-GkTWPhXBSH6y7ML?usp=sharing

# Code working:
We Rpi.GPIO library python to get input from button .
When button is pressed then firebase notification value is set to 1. and the notification is send to every body

# Video Streaming :

# Tech used:
  1:picamera
  2:firebase Storage
       
# Purpose:
   The acquaintance is concerned about where the user
           is going or what is happening to him/her. They can see
          that information easily on their screen.
# Working:
We break the video in chunks of 5 sec. Recording of each 5  sec is uploaded on the cloud then it is retrieved for broadcasting.While streaming we extract the latest video uploaded and play on HTML5 video player

# Code:
https://drive.google.com/drive/folders/1h-xIcImSAWutJAe-YWTN_nXfN9FteJJv?usp=sharing

# 4. Voice Navigation
	
# Objective:
Helping a old or a blind person to navigate wherever he      wants to go .

# Problem solved:
A old person and a blind person generally cant use smart phone. If he has to navigate somewhere then they have no option left other than depending on other. So in this feature of mine he only needs to say where he wants to go and he will reach to his destination.
	
# Equipment Used:
	1:  Microphone
	2:  Speaker
	
# Tech Used:
	1:  Speech To Text (google api)
	2:  Google maps api
	3:  Text to Speech (google api)

# Working:
we are using google api speech to text ,to get input from the user. Then we pass it to google map api, which returns a json object containing tons of data. We filter it out according to user choice then extract the direction and distance . Then we used text to speech to give audio output to user through speaker(earphone).

# Code:
https://drive.google.com/drive/folders/1l0yktGm7Jmx9btwhH01KPqug5OecpG7H?usp=sharing


# 5 . Real-Time object Detection
	
# Objective:
Inform the user about any obstacle that is in front of him(car,stair,bike,chair etc). 

# Problem solved :
For Blind people and people with less vision they have tough time traveling without help so we are using image processing to inform the user about any obstacle that come in front of him

# Tech Used:
1: Open CV
2: Kaggle trainner

# Working:
Now Image processing in itself a big topic . We used Haarcascade method for detection it relatively easy and take less time to train but it is slow and less accurate .
So first we pick the data set of negative images which include 5000+ image of different situation . Then we stick to the image for which we have to train on these images and convert it into positive images thus we have a set of image for object in different situation then we train it with opencv to a different higher level of more accuracy but it takes more time. I went to 24th level it took 6 days to train on cloud  with accuracy of 53.264%. 

we used imutils to resize the frame captured by the opencv.video(src=0). Then we check the frame with xml file from our trained data. If it recognises by accuracy of 30 % then we play the message in speaker/earphone .

# Code:
https://drive.google.com/drive/folders/1F7n_8oqhO46stGWa1wS_yEXRACM-PTtm?usp=sharing


the code consist of two files in which the stair.py  for stairs detection and detection.py for other.

# Limitation :

Right now we are limited with knowledge , time  and resource .
1:Raspberry pi heats up after running detection code and it has slow processor. 
2:We don’t have time and resource to train model for better accuracy . 
3:We are in  beginner phase of image processing so we are unable to make efficient model for dataset. Tough time finding dataset.




# Future Scope :

With Proper processor like the one our phone has we are able to process data much faster. Now if we are able to train data such that it can detect the object with greater accuracy which is not impossible. Tesla cars are already doing that. With proper resource , time and knowledge we can give a blind person a virtual eye and an assistant/companion which tells how to avoid collision  when an object is coming towards him with a certain distance , velocity and direction  .The user can interact with it asking about weather and direction etc like google assistant. It is just an attachment to the stick which is not at all bulky or heavy with just a camera, processor and battery.



# With this device we want to give visually challenged people the liberty to be independent, to be free to go wherever they want to  without any help. To see the world virtually with advanced technology. And most importantly to provide them with security .
