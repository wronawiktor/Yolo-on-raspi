import cv2
from ultralytics import YOLO

model=YOLO('best.pt')
        
cv2.namedWindow('RGB')
cap=cv2.VideoCapture(0)

count = 0
while True:    
    ret,frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame=cv2.resize(frame,(640,480))

    results=model.predict(frame, conf=0.5)
    res_plotted = results[0].plot()

    cv2.imshow("RGB", res_plotted)
    if cv2.waitKey(1)&0xFF==27:
        break
    
cap.release()
cv2.destroyAllWindows()