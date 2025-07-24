import mediapipe as mp
import pyautogui as pg
import cv2
import winsound

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection()
video=cv2.VideoCapture(0)
n=4
correct_position=None

threshold1=45 # minimum range for eye ear distance 
threshold2=57 # maximum range for eye ear distance
while True:
  suc,img=video.read()
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  lx,ly,rx,ry=245,150,490,400
  h,w,_=img.shape

  c=(0,0,255)
  if not result.detections:
    c=(0,0,255)
    sentence='No face detected'
  else:
    for detection in result.detections:
      right_eye=detection.location_data.relative_keypoints[0]
      left_eye=detection.location_data.relative_keypoints[1]
      nose_tip=detection.location_data.relative_keypoints[2]
      mouth_center=detection.location_data.relative_keypoints[3]
      right_ear=detection.location_data.relative_keypoints[4]
      left_ear=detection.location_data.relative_keypoints[5]


      r_ear_x=right_ear.x
      r_ear_y=right_ear.y
      r_eye_x=right_eye.x
      r_eye_y=right_eye.y
      l_ear_x=left_ear.x
      l_ear_y=left_ear.y
      l_eye_x=left_eye.x
      l_eye_y=left_eye.y
      left_eye_ear_dist=((((l_eye_x-l_ear_x)**2)*w*w) + (((l_eye_y-l_ear_y)**2)*h*h))**(0.5)
      right_eye_ear_dist=((((r_eye_x-r_ear_x)**2)*w*w) + (((r_eye_y-r_ear_y)**2)*h*h))**(0.5)
      print(left_eye_ear_dist)
      if right_ear.x > right_eye.x or left_ear.x < left_eye.x or right_eye.y>=right_ear.y:
        correct_position=False
        if right_ear.x > right_eye.x:
          print('Head turns right')
        if left_ear.x < left_eye.x:
          print('Head turns left')
        if right_eye.y>=right_ear.y:
          print("Head turns downwards")
        c=(0,0,255)
        winsound.Beep(1000,500)
        sentence="Unauthorized activity detected."
      else:
        c=(72,114,0)
        sentence=f'{n} chances to continue the Interview'
        if left_eye_ear_dist<threshold1 or left_eye_ear_dist>threshold2 or right_eye_ear_dist<threshold1 or right_eye_ear_dist>threshold2:
          c=(0,0,255)
          sentence='Eye is not aligned straight'
          # winsound.Beep(1000,500)

      
      if int(right_ear.x*w)<lx or int(left_ear.x*w)>rx or int(mouth_center.y*h)>ry or int(left_eye.y*h)<ly or int(right_eye.y*h)<ly:
        c=(0,0,255)
        sentence="Face not aligned properly"
        if right_ear.x > right_eye.x or left_ear.x < left_eye.x or right_eye.y>=right_ear.y or left_eye_ear_dist<threshold1 or left_eye_ear_dist>threshold2 or right_eye_ear_dist<threshold1 or right_eye_ear_dist>threshold2:
          sentence="Unauthorized activity detected."

      
      if correct_position==False and right_ear.x < right_eye.x and left_ear.x > left_eye.x and right_eye.y < right_ear.y:
        correct_position=True
        n-=1

      
      if n==0:
        c=(255,255,255)
        sentence="Distraction Limit Exceeded"
      # mpdrawings.draw_detection(img,detection)
  cv2.rectangle(img,(lx,ly),(rx,ry),c,3)
  cv2.putText(img,sentence,(30,30),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale=0.9,color=c,thickness=3)
  if n==0:
    img=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cv2.imshow('EXAM',img)
    cv2.waitKey(3800)
    pg.press('q')
    break
  cv2.imshow('EXAM',img)
  if cv2.waitKey(1) & 0XFF==ord('q'):
    break
video.release()
cv2.destroyAllWindows()
