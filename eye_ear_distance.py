import mediapipe as mp
import cv2

mpfaces=mp.solutions.face_detection
mpdrawings=mp.solutions.drawing_utils

faces=mpfaces.FaceDetection()

video=cv2.VideoCapture(0)
while True:
  suc,img=video.read()
  img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
  result=faces.process(img1)
  h,w,_=img.shape
  if result.detections:
    for detection in result.detections:
      right_eye=detection.location_data.relative_keypoints[0]
      left_eye=detection.location_data.relative_keypoints[1]
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
      l_eye_ear_dist=((((l_eye_x-l_ear_x)**2)*w*w) + (((l_eye_y-l_ear_y)**2)*h*h))**(0.5)
      
      print(l_eye_ear_dist)
      mpdrawings.draw_detection(img,detection)
  cv2.imshow("Image",img)
  if cv2.waitKey(1) & 0XFF==113:
    break
video.release()
cv2.destroyAllWindows()


# it is concluded that the eye ear distance is calculated as when face is staright towards the webcame
