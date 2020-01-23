import cv2
import trackerFunc as tF
import rodTusjDetection as rtd
import numpy as np

def makePoint(bbox):
    p1 = (int(bbox[0]) + int(bbox[1]))*0.5
    p2 = (int(bbox[2]) + int(bbox[3]))*0.5
    return [p1,p2]


tracker = tF.createTrackerByName(tF.types[3])

track = []

video = cv2.VideoCapture(0) # Read video
ok, frame = video.read()
frame = rtd.redProsessFrame(frame)
frame = np.stack((frame,)*3, axis=-1)

# Define an initial bounding box
bbox = (287, 23, 86, 320)
# Uncomment the line below to select a different bounding box
bbox = cv2.selectROI(frame, False)
track.append(track, makePoint(bbox))
# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)

while(True):
    ok, frame = video.read()
    frame = rtd.redProsessFrame(frame)
    frame = np.stack((frame,)*3, axis=-1)

    if not ok:
        print('im hurt :(')
        break
    
    # Start timer
    timer = cv2.getTickCount()
 
    # Update tracker
    ok, bbox = tracker.update(frame)
    track.append(makePoint(bbox))

    if(len(track) > 100):
       track.delete(track, [100])
    # Draw bounding box
    if ok:
    # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

        for i in range(0, len(track)-1):
            #cv2.line(frame, track[i], track[i+1], (0,0,255), 10)
            
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
    
    cv2.imshow("Tracking", frame)

    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27 : break

cv2.destroyWindow("Tracking")