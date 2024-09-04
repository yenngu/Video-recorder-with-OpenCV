import cv2 as cv
import numpy as np
import datetime
import time

# Capture Camera
videoCapture = cv.VideoCapture(0)

#Convert to codec
video_format = cv.VideoWriter_fourcc(*'MP4V')

#Write video frames into a file
video_FPS = 60.0
video_Size = (int(videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)),
              int(videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)))

# Font
font = cv.FONT_HERSHEY_SIMPLEX

#Detection Variables
human_model = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_fullbody.xml')
face_model = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')

def detectHuman(frame):
    human = human_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    facehuman = face_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    
    detected = False
    
    for(x,y,w,h) in human:
        cv.rectangle(frame, (x,y), (x+w, y+h), (100,0,0), 2)
        cv.putText(frame, 'Human', (x + 6, y - 6), font, 0.5,(100, 0 ,0), 1)
        detected = True
        
    for(x,y,w,h) in facehuman:
        cv.rectangle(frame, (x,y), (x+w, y+h), (100,0,0), 2)
        cv.putText(frame, 'Face', (x + 6, y - 6), font, 0.5,(100, 0 ,0), 1)
        detected = True
        
    return frame, detected

def grabTime():
    currentDate = datetime.datetime.now()
    date_string = currentDate.strftime('%m/%d/%Y')
    time_string = currentDate.strftime('%H:%M:%S')
    return date_string,time_string

record = False
record_delay = 15
last_detected = False

# While True Capture Camera frame by frame
while True:
    ret, frame = videoCapture.read()

    if not ret:
        print("Error no ret")
        break
    
    #Grab variables from function
    
    frame, detected = detectHuman(frame)
    
    #Grab current time for calculation
    
    date_string, time_string = grabTime()
    current_time = time.time()
    
    #save video if detected
    if detected:
        if not record:
            write_video = cv.VideoWriter(f'{date_string}.{time_string}', video_format, video_FPS, video_Size)
            record = True
            last_detected = True
            time_at_detection = current_time
            print("Security footage recording started.")
            
    if record:
        write_video.write(frame)
        
        if last_detected is not None and (current_time - time_at_detection) >= record_delay:
            write_video.release()
            record = False
            print("Security footaved saved.")
    
    # Show date time
    cv.putText(frame, f'Time: {time_string}, Date: {date_string}', (0, 25), font, .75, (0,0,0), 2, cv.LINE_AA)    
    # Show Frame
    cv.imshow('frame', frame)    
    
    # Close Frame Button With ASCII 'ESC'
    if cv.waitKey(1) &0XFF == 27:
        break

videoCapture.release()
cv.destroyAllWindows()
    