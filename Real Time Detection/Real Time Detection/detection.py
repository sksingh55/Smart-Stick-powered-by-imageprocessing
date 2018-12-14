from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import textspeech
import stair
import os



args = {'model': 'MobileNetSSD_deploy.caffemodel', 'confidence': 0.2, 'prototxt': 'MobileNetSSD_deploy.prototxt.txt'}
print(args)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor","staircase"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

_object=""
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()


frame = vs.read()
frame = imutils.resize(frame, width=400)
stair.main(frame)
(h, w) = frame.shape[:2]

blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
	0.007843, (300, 300), 127.5)


net.setInput(blob)
detections = net.forward()


for i in np.arange(0, detections.shape[2]):

	confidence = detections[0, 0, i, 2]
	if confidence > args["confidence"]:
		idx = int(detections[0, 0, i, 1])
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		if CLASSES[idx]!= _object:
			print(CLASSES[idx])
			_object=CLASSES[idx]
			if (_object=="car"):
				os.system("mpg321 car.mp3")
			if (_object=="bottle"):
				os.system("mpg321 bottle.mp3")
			if (_object=="bike"):
				os.system("mpg321 bike.mp3")
			if (_object=="cat"):
				os.system("mpg321 cat.mp3")
			if (_object=="dog"):
				os.system("mpg321 dog.mp3")
			if (_object=="person"):
				os.system("mpg321 person.mp3")
			if (_object=="diningtablr"):
				os.system("mpg321 table.mp3")
key = cv2.waitKey(1) & 0xFF

fps.update()


fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cv2.destroyAllWindows()
vs.stop()
