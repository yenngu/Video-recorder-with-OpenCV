import cv2 as cv;
import numpy as np;
import datetime

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

detected = False

def detectHuman(frame):
    human = human_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    facehuman = face_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    for(x,y,w,h) in human:
        cv.rectangle(frame, (x,y), (x+w, y+h), (100,0,0), 2)
        cv.putText(frame, 'Human', (x + 6, y - 6), font, 0.5,(100, 0 ,0), 1)
    for(x,y,w,h) in facehuman:
        cv.rectangle(frame, (x,y), (x+w, y+h), (100,0,0), 2)
        cv.putText(frame, 'Face', (x + 6, y - 6), font, 0.5,(100, 0 ,0), 1)
    return frame
    
# While True Capture Camera frame by frame
while True:
    ret, frame = videoCapture.read()

    if not ret:
        print("Error no ret")
        break
    
    # Grab current date and time
    currentDate = datetime.datetime.now()
    date = currentDate.strftime('%m/%d/%Y')
    time = currentDate.strftime('%H:%M:%S')
    
    
    #video save format
    write_video = cv.VideoWriter(f'{date}.{time}', video_format, video_FPS, video_Size)
    
    # Show date time
    cv.putText(frame, f'Time: {time}, Date: {date}', (0, 25), font, .75, (0,0,0), 2, cv.LINE_AA)
    
    frame = detectHuman(frame)
    
    # Show Frame
    cv.imshow('frame', frame)    
    
    write_video.write(frame)
    
    # Close Frame Button With ASCII 'ESC'
    if cv.waitKey(1) &0XFF == 27:
        break


write_video.release()
videoCapture.release()
cv.destroyAllWindows()
    