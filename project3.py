import numpy as np
import cv2

cap = cv2.VideoCapture(0)
fist_cascade =cv2.CascadeClassifier('fist.xml')
while(True):

	ret, frame = cap.read()
		
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	fist=fist_cascade.detectMultiScale(gray,1.3,5)
	for(x,y,w,h) in fist:
		cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
	
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
			break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()