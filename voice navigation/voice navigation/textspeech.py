# Import the required module for text 
# to speech conversion 
from gtts import gTTS  
import os 
def main(var):
	print("enter")
	mytext = var
	language = 'en' 
	myobj = gTTS(text=mytext, lang=language, slow=False) 
	myobj.save("welcome.mp3") 
	os.system("mpg321 welcome.mp3") 
	print("exit")
