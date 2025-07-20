import mediapipe as mp
import pyautogui as pg
import cv2
import winsound

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection()
w="Unauthorized activity detected."
video=cv2.VideoCapture(0)
n=5
correct_position=None
while True:
  suc,img=video.read()
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  cv2.rectangle(img,(160,80),(390,400),(0,0,255),2)
  if result.detections:
    for detection in result.detections:
      right_eye=detection.location_data.relative_keypoints[0]
      left_eye=detection.location_data.relative_keypoints[1]
      right_ear=detection.location_data.relative_keypoints[4]
      left_ear=detection.location_data.relative_keypoints[5]
      if right_ear.x > right_eye.x or left_ear.x < left_eye.x:
        correct_position=False
        if right_ear.x > right_eye.x:
          print('Head turns right')
        if left_ear.x < left_eye.x:
          print('Head turns left')
        winsound.Beep(700,100)
        cv2.putText(img,w,(30,30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=1,color=(0,0,255),thickness=2)
      else:
        cv2.putText(img,f'{n} chances to continue the exam',(30,30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.9,color=(255,255,0),thickness=2)
      if correct_position==False and right_ear.x < right_eye.x and left_ear.x > left_eye.x:
        correct_position=True
        n-=1
      if n==0:
        cv2.putText(img,'Distraction Limit Exceeded',(30,50),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.9,color=(0,0,255),thickness=2)
        cv2.imshow('EXAM',img)
        cv2.waitKey(5000)
        pg.press('q')
        break
      mpdrawings.draw_detection(img,detection)
  cv2.imshow('EXAM',img)
  if cv2.waitKey(1) & 0XFF==ord('q'):
    break
video.release()
cv2.destroyAllWindows()
