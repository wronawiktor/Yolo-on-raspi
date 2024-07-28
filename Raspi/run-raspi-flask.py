import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
from flask import Flask, render_template, Response

app = Flask(__name__)
model=YOLO('best.onnx')
piCam=Picamera2()
piCam.preview_configuration.main.size=(640, 384)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.main.align()
piCam.start()

@app.route('/')
def index():
    return render_template('index.html')

def gen():

    while True:
        frame=piCam.capture_array()
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