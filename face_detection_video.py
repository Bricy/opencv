# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import serial 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 	faces = face_cascade.detectMultiScale(gray, 1.1, 5)

 	for (x,y,w,h) in faces:
 		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
 		cv2.putText(image, str(x)+','+str(y), (x+w/2,y+h/2),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
	# show the frame

	data = transmit(x,y,w,h)
	s=serial.Serial('/dev/ttyACM0',9600)
	s.write(data)

	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("p"):
		break

#transmit data to arduino
def transmit(x,y,w,h):
	framex=320                # the x coordinate center of the frame
	framey=240			   # the y coordinate center of the frame
	comx=x+w/2
	comy=y+h/2
	if comx<framex:
		direction='L'
		degree=float(framex-comx)/320 
	else:
		direction='R'
		degree=float(comx-framex)/320

	degree=int(1000*round(degree,3));
	if (degree<10):
		res=str(00)+str(degree)
	elif (degree<100):
		res=str(0)+str(degree)
	else:
		res=str(degree)
	data=direction+res
	print data