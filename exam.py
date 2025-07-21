import mediapipe as mp
import pyautogui as pg
import cv2
import winsound

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection()
video=cv2.VideoCapture(0)
n=10
correct_position=None
while True:
  suc,img=video.read()
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  lx,ly,rx,ry=245,150,490,400
  h,w,_=img.shape
  cv2.rectangle(img,(lx,ly),(rx,ry),(0,0,255),3)

  c=(0,0,255)
  sentence='NO face detected'
  if result.detections:
    for detection in result.detections:
      right_eye=detection.location_data.relative_keypoints[0]
      left_eye=detection.location_data.relative_keypoints[1]
      nose_tip=detection.location_data.relative_keypoints[2]
      mouth_center=detection.location_data.relative_keypoints[3]
      right_ear=detection.location_data.relative_keypoints[4]
      left_ear=detection.location_data.relative_keypoints[5]
      if right_ear.x > right_eye.x or left_ear.x < left_eye.x or right_eye.y>=right_ear.y:
        correct_position=False
        if right_ear.x > right_eye.x:
          print('Head turns right')
        if left_ear.x < left_eye.x:
          print('Head turns left')
        if right_eye.y>=right_ear.y:
          print("Head turns downwards")
        c=(0,0,255)
        winsound.Beep(700,100)
        sentence="Unauthorized activity detected."
      else:
        c=(0,255,0)
        sentence=f'{n} chances to continue the exam'
      if int(right_ear.x*w)<lx or int(left_ear.x*w)>rx or int(mouth_center.y*h)>ry or int(left_eye.y*h)<ly or int(right_eye.y*h)<ly:
        c=(0,0,255)
        sentence="Face not aligned properly"
      if correct_position==False and right_ear.x < right_eye.x and left_ear.x > left_eye.x and right_eye.y < right_ear.y:
        correct_position=True
        n-=1
      if n==0:
        c=(0,0,255)
        sentence="Distraction Limit Exceeded"
      cv2.rectangle(img,(lx,ly),(rx,ry),c,3)
      cv2.putText(img,sentence,(30,30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.9,color=c,thickness=3)
      if n==0:  
        cv2.imshow('EXAM',img)
        cv2.waitKey(5000)
        pg.press('q')
        break
  cv2.imshow('EXAM',img)
  if cv2.waitKey(1) & 0XFF==ord('q'):
    break
video.release()
cv2.destroyAllWindows()
