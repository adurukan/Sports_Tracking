import numpy as np
import cv2
import time
class tracking():
    def loadFile(fileName):
        global cap
        cap = cv2.VideoCapture(fileName)
        global circle
        circle = []
        global pt2, pt3
        pt2 = (0,0)
        pt3 = (0,0)
        loaded = True
        return loaded

    def draw_circle(event, x, y, flags, param):
        global pt1, circle
        # get mouse click on down and track center
        if event == cv2.EVENT_LBUTTONDOWN:
            pt1 = (x, y)
            circle.append(pt1)
        # Use boolean variable to track if the mouse has been released
        if event == cv2.EVENT_RBUTTONDOWN:
            cv2.destroyWindow("Select Set Points")

    def draw_rectangle(event, x, y, flags, param):
        global pt2, pt3
        # get mouse click on down and track center
        if event == cv2.EVENT_LBUTTONDOWN:
            pt2 = (x,y)
        # Use boolean variable to track if the mouse has been released
        if event == cv2.EVENT_RBUTTONDOWN:
            pt3 = (x,y)
            print(pt2, pt3)
            cv2.waitKey(1)
            cv2.destroyWindow("Select Points on the Field")

    def create_blank(width, height):
        """Create new image(numpy array) filled with certain color in RGB"""
        # Create black blank image
        image = np.ones((height, width, 3), np.uint8)*255
        return image

    #Procedures run on the first frame
    def mapping():
        ret, frame = cap.read()

        global trackers
        trackers = cv2.MultiTracker_create()
        fromCenter = False
        tracker_types = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE']
        tracker_type = tracker_types[5]

        #Window for selecting base coordinates for transformation
        cv2.namedWindow("Select Set Points", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        cv2.moveWindow("Select Set Points", 200, 170)
        cv2.resizeWindow("Select Set Points", 900, 580)
        cv2.setMouseCallback("Select Set Points", tracking.draw_circle)
        cv2.imshow("Select Set Points", frame)
        cv2.waitKey(0)

        #Window for selecting reflection coordiantes for transformation
        static = cv2.imread("assets/halisaha.png")
        cv2.namedWindow("Select Points on the Field", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        cv2.moveWindow("Select Points on the Field", 1140, 235)
        cv2.resizeWindow("Select Points on the Field", 512, 341)
        cv2.setMouseCallback("Select Points on the Field", tracking.draw_rectangle)
        cv2.imshow("Select Points on the Field", static)
        cv2.waitKey(0)

        #Coordinates for the perspective transform function
        global w1,h1,pts1,pts2
        w1 = int(circle[1][0]-circle[0][0])
        h1 = int(circle[2][1]-circle[0][1])
        pts1 = np.float32([[circle[0]], [circle[1]], [circle[2]], [circle[3]]])
        pts2 = np.float32([[0, 0], [w1, 0], [0, h1], [w1, h1]])

        global matrix
        matrix = cv2.getPerspectiveTransform(pts1,pts2)

        #Window for Region of Interest Selection
        cv2.namedWindow("Select Players", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions
        cv2.moveWindow("Select Players", 230, 160)
        cv2.resizeWindow("Select Players", 900, 580)
        k = 3
        for i in range(k):
            r = cv2.selectROI("Select Players", frame, fromCenter)
            trackers.add(cv2.TrackerCSRT_create(), frame, r)
        cv2.destroyWindow("Select Players")

        return frame, pt2, pt3, w1, h1

    #Returning original frame and tracking
    def running():
        # Capture frame-by-frame
        ret, frame = cap.read()
        (success, boxes) = trackers.update(frame)

        #for box in boxes:
        (tx, ty, tw, th) = [int(a) for a in boxes[0]]
        cv2.rectangle(frame, (tx, ty), (tx + tw, ty + th), (0, 0, 255), 2)
        (x, y, w, h) = [int(a) for a in boxes[1]]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        (ax, ay, aw, ah) = [int(a) for a in boxes[2]]
        cv2.rectangle(frame, (ax, ay), (ax + aw, ay + ah), (255, 0, 0), 2)

        #Creating boxes for tracked positions of players
        frame2 = tracking.create_blank(frame.shape[1], frame.shape[0])
        frame2[:,:] = [150, 150, 150]
        frame2[ty + th+0:ty + th+40,tx + tw - 20:tx + tw+20, :] = [0, 0, 255]
        frame2[y + h+10:y + h+50, x + w - 20:x + w+20, :] = [0, 0, 255]
        frame2[ay + ah+10:ay + ah+50, ax + aw - 20:ax + aw+20, :] = [255, 0, 0]

        #Transforming image to bird-eye perspective
        frame3 = cv2.warpPerspective(frame2, matrix, (w1, h1))

        return frame, frame3

