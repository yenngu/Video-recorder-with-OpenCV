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
write_video = cv.VideoWriter('', video_format, video_FPS, video_Size)

# Font
font = cv.FONT_HERSHEY_SIMPLEX

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
    
    # Show date time
    cv.putText(frame, f'Time: {time}, Date: {date}', (0, 25), font, .75, (0,0,0), 2, cv.LINE_AA)
    
    # Show Frame
    cv.imshow('frame', frame)
    
    # Show Date/Time
    
    
    write_video.write(frame)
    
    
    
    # Close Frame Button With ASCII 'ESC'
    if cv.waitKey(1) &0XFF == 27:
        break


write_video.release()
videoCapture.release()
cv.destroyAllWindows()
    