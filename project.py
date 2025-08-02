import mediapipe as mp
import pyautogui as pg
import cv2
import winsound

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection()



def detection_findings(img):
  findings_dict={}
  status=False
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  h,w,_=img.shape
  if result.detections:
    status=True
    for detection in result.detections:
      right_eye=detection.location_data.relative_keypoints[0]
      left_eye=detection.location_data.relative_keypoints[1]
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
      mouth_y=mouth_center.y
      l_eye_ear_dist=((((l_eye_x-l_ear_x)**2)*w*w) + (((l_eye_y-l_ear_y)**2)*h*h))**(0.5)
      r_eye_ear_dist=((((r_eye_x-r_ear_x)**2)*w*w) + (((r_eye_y-r_ear_y)**2)*h*h))**(0.5)
      findings_dict={'l_eye_ear_dist':l_eye_ear_dist,'r_eye_ear_dist':r_eye_ear_dist,'r_ear_x':r_ear_x,'r_ear_y':r_ear_y,'r_eye_x':r_eye_x,'r_eye_y':r_eye_y,'l_ear_x':l_ear_x,'l_ear_y':l_ear_y,'l_eye_x':l_eye_x,'l_eye_y':l_eye_y,'mouth_y':mouth_y}
  findings_dict['status']=status
  return findings_dict


video=cv2.VideoCapture(0)
num=0
l=[]
scan_y=150
direction=1
while True:
  suc,img=video.read()
  lx,ly,rx,ry=245,150,490,400
  findings_dict=detection_findings(img)
  if findings_dict['status']==False:
    c=(0,0,255)
    sentence='No face detected'
  else:
    l_eye_ear_dist=findings_dict['l_eye_ear_dist']
    r_eye_ear_dist=findings_dict['r_eye_ear_dist']
    if abs(l_eye_ear_dist-r_eye_ear_dist)>5: # to avoid the customized format of eye and year distance
      sentence='Look into the camera'
      c=(0,0,255)
      pass
    else:
      sentence='Move your head frontward and backward'
      c=(72,114,0)
      l.append((l_eye_ear_dist+r_eye_ear_dist)/2)
      num+=1
  cv2.putText(img,sentence,(30,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,c,thickness=3)
  cv2.rectangle(img,(lx,ly),(rx,ry),c,3)
  cv2.line(img, (lx, scan_y), (rx, scan_y), (0, 255, 255), 2)

  scan_y += direction * 2
  if scan_y >= ry or scan_y <= ly:
    direction *= -1 
  cv2.imshow("Image",img)
  if cv2.waitKey(1) & 0XFF==113:
    break
video.release()
cv2.destroyAllWindows()

threshold1=min(l)
threshold2=max(l)
print('min_threshold:',threshold1)
print('max_threshold:',threshold2)

video=cv2.VideoCapture(0)
n=5
correct_position=None
while True:
  suc,img=video.read()
  lx,ly,rx,ry=245,150,490,400
  c=(0,0,255)
  h,w,_=img.shape
  findings_dict=detection_findings(img)
  if findings_dict['status']==False:
    c=(0,0,255)
    sentence='No face detected'
  else:
    l_eye_ear_dist=findings_dict['l_eye_ear_dist']
    r_eye_ear_dist=findings_dict['r_eye_ear_dist']
    r_ear_x=findings_dict['r_ear_x']
    r_ear_y=findings_dict['r_ear_y']
    r_eye_x=findings_dict['r_eye_x']
    r_eye_y=findings_dict['r_eye_y']
    l_ear_x=findings_dict['l_ear_x']
    l_ear_y=findings_dict['l_ear_y']
    l_eye_x=findings_dict['l_eye_x']
    l_eye_y=findings_dict['l_eye_y']
    mouth_y=findings_dict['mouth_y']
    print(l_eye_ear_dist)
    print(r_eye_ear_dist)
    if r_ear_x > r_eye_x or l_ear_x < l_eye_x or r_eye_y>=r_ear_y:
      correct_position=False
      if r_ear_x > r_eye_x:
        print('Head turns right')
      if l_ear_x < l_eye_x:
        print('Head turns left')
      if r_eye_y>=r_ear_y:
        print("Head turns downwards")
      c=(0,0,255)
      winsound.Beep(1000,500)
      sentence="Unauthorized activity detected."
    else:
      c=(72,114,0)
      sentence=f'{n} chances to continue the Interview'
      if l_eye_ear_dist<threshold1 or l_eye_ear_dist>threshold2 or r_eye_ear_dist<threshold1 or r_eye_ear_dist>threshold2:
        c=(0,0,255)
        sentence='Eye is not aligned straight'
        # winsound.Beep(1000,500)

      
      if int(r_ear_x*w)<lx or int(l_ear_x*w)>rx or int(mouth_y*h)>ry or int(l_eye_y*h)<ly or int(r_eye_y*h)<ly:
        c=(0,0,255)
        sentence="Face not aligned properly"
        if r_ear_x > r_eye_x or l_ear_x < l_eye_x or r_eye_y>=r_ear_y or l_eye_ear_dist<threshold1 or l_eye_ear_dist>threshold2 or r_eye_ear_dist<threshold1 or r_eye_ear_dist>threshold2:
          sentence="Unauthorized activity detected."

      
      if correct_position==False and r_ear_x < r_eye_x and l_ear_x > l_eye_x and r_eye_y < r_ear_y:
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