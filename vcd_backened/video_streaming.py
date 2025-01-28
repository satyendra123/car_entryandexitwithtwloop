'''
import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

camera_url = "rtsp://admin:dsal@123@192.168.1.113:554/cam/realmonitor?channel=1&subtype=1"
camera_name="ENTRY"


def generate_frames():
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print(f"Unable to open video capture for {camera_name}")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture frame from {camera_name}")
            time.sleep(5)  # Wait before retrying
            cap = cv2.VideoCapture(camera_url)  # Reinitialize capture
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return 
        <html>
        <body>
            <h1>IP Camera Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
        </html>
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
'''


import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

camera_name = "System Camera"  # Set a name for your local camera


def generate_frames():
    cap = cv2.VideoCapture('rtsp://admin:dsal@123@192.168.1.113:554/cam/realmonitor?channel=1&subtype=0')  # Use 0 for the default system camera
    if not cap.isOpened():
        print(f"Unable to open video capture for {camera_name}")
        return
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture frame from {camera_name}")
            time.sleep(5)  # Wait before retrying
            cap = cv2.VideoCapture(0)  # Reinitialize capture
            continue
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame in MJPEG format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '''
        <html>
        <body>
            <h1>System Camera Stream</h1>
            <img src="/video_feed" width="640" height="480">
        </body>
        </html>
    '''
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
