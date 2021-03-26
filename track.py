import numpy as np
import cv2
import time

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
print(cv2.__version__)

#Capturing the video
cap = cv2.VideoCapture('futbol.mp4')
#Reading the video frame by frame
fromCenter = False
ret, frame = cap.read()
r=(0,0,0,0)
r = cv2.selectROI('Test', frame, fromCenter)

tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
tracker_type = tracker_types[5]

if int(major_ver) < 4 and int(minor_ver) < 3:
    tracker = cv2.cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'CSRT':
        tracker = cv2.TrackerCSRT_create()
    if tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()

ret = tracker.init(frame, r)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break

    ret, r = tracker.update(frame)

    # Use if statement to see if clicked is true
    p1 = (int(r[0]), int(r[1]))
    p2 = (int(r[0] + r[2]), int(r[1] + r[3]))
    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

    # Display the resulting frame
    cv2.imshow('Test', frame)
    #time.sleep(1 / 2)

    # This command let's us quit with the "q" button on a keyboard.
    # Simply pressing cdX on the window won't work!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

