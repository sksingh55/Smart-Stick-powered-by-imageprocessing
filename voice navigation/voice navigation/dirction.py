import urllib.request, json
import textspeech
import lastlocation
import speech_recognition as sr
import os
import dirction
import textspeech

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyB5U6iCtTTkLHH576hV7Zbx-2hTAOq3tts'
def main(des):
		
	origin = str(lastlocation.address())
	origin = origin.replace(' ','+')
	destination = des.replace(' ','+')

	nav_request = 'origin={}&destination={}&key={}'.format(origin,destination,api_key)
	request = endpoint + nav_request
	response = urllib.request.urlopen(request).read()
	directions = json.loads(response)
	try:
		routes = directions['routes']
		print(routes[0])
		for i in range(len(routes[0]['legs'][0]['steps'])):
			s=routes[0]['legs'][0]['steps'][i]['html_instructions']
			end = routes[0]['legs'][0]['steps'][i]['end_location']
			print(end)
			cur=lastlocation.get()
			endlng = end['lng']
			endlat = end['lat']
			curlng = cur['long']
			curlat = cur['lat']
			acc = abs(curlat-endlat)/endlat * abs(curlng-endlng)/endlat
			print(acc)
			command=""
			j=0
			while j<(len(routes[0]['legs'][0]['steps'][i]['html_instructions'])):
				if(s[j] == '<'):
					command = command + " "
					while s[j]!='>':
						j = j+1
				else:
					command = command + s[j]
				j = j+1
			command = command + "and walk for distance of "+routes[0]['legs'][0]['steps'][i]['distance']['text']
			textspeech.main(command)
			while acc<1:
				r2=sr.Recognizer()
				x2 = ""
				with sr.Microphone() as source2:
					print("say something")
					audio2 = r2.listen(source2)
					print("time over")
					x2=r2.recognize_google(audio2)
					dirction.main(x2)
				if "stop" in x2:
					return
				cur=lastlocation.get()
				endlng = end['lng']
				endlat = end['lat']
				curlng = cur['long']
				curlat = cur['lat']
				acc = abs(curlat-endlat)/endlat * abs(curlng-endlng)/endlat
				print(acc)
	except:
		textspeech.main("show cant find the location")
		return



