from flask import Flask, render_template, Response
import cv2
from ultralytics import YOLO

app = Flask(__name__)
model=YOLO('best.pt')
cap=cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen():

    while True:
        ret, frame = cap.read()
        frame=cv2.resize(frame,(640,480))
        results=model.predict(frame, conf=0.5, verbose=False)
        res_plotted = results[0].plot()

        _, buffer=cv2.imencode('.jpg',res_plotted)
        output=buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)