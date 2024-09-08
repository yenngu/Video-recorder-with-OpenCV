from flask import Flask, jsonify, render_template, Response, send_from_directory
import cv2 as cv
import numpy as np
import datetime
import time
import os

main = Flask(__name__)

# Capture Camera
videoCapture = cv.VideoCapture(0)

# Font
font = cv.FONT_HERSHEY_SIMPLEX

# Detection Variables
human_model = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_fullbody.xml')
face_model = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_alt.xml')

def detectHuman(frame):
    human = human_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    facehuman = face_model.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
    
    detected = False
    
    for (x, y, w, h) in human:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 175), 2)
        cv.putText(frame, 'Human', (x + 6, y - 6), font, 0.5, (0, 0, 175), 1)
        detected = True
        
    for (x, y, w, h) in facehuman:
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 175), 2)
        cv.putText(frame, 'Face', (x + 6, y - 6), font, 0.5, (0, 0, 175), 1)
        detected = True
        
    return frame, detected

def grabTime():
    currentDate = datetime.datetime.now()
    date_string = currentDate.strftime('%m_%d_%Y')
    time_string = currentDate.strftime('%H_%M_%S')
    return date_string, time_string

# Recording
video_FPS = int(videoCapture.get(cv.CAP_PROP_FPS))
video_Size = (int(videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)), 
              int(videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)))

fourcc = cv.VideoWriter_fourcc(*'mp4v')
record_Video = None
time_record = 0
record_delay = 5
record = False

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/start_recording')
def start_recording():
    global record, time_record, record_Video
    date_string, time_string = grabTime()
    file_string = f"video_storage/{date_string}_{time_string}.mp4"
    record_Video = cv.VideoWriter(file_string, fourcc, video_FPS, video_Size)
    record = True
    time_record = time.time()
    return jsonify("Recording started.")

@main.route('/stop_recording')
def stop_recording():
    global record, record_Video
    if record:
        record = False
        record_Video.release()
        record_Video = None
        return jsonify("Recording Stopped.")
    else:
        return jsonify("No recording in progress.")

@main.route('/video_feed')
def video_feed():
    def generate():
        while True:
            success, frame = videoCapture.read()
            if not success:
                break
            
            frame, _ = detectHuman(frame)
            
            # Encode frame as JPEG
            ret, jpeg = cv.imencode('.jpg', frame)
            if not ret:
                break
            
            # Yield the frame in the required format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@main.route('/list_videos')
def list_videos():
    files = [f for f in os.listdir('video_storage') if f.endswith('.mp4')]
    files.sort(reverse=True)
    return jsonify(files)

@main.route('/video_storage/<filename>')
def serve_video(filename):
    return send_from_directory('video_storage', filename)

if __name__ == '__main__':
    main.run(debug=True)
