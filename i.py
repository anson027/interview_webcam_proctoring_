import cv2
import mediapipe as mp

# Initialize MediaPipe face detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Set up face detection with confidence threshold
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        h,w,_=frame.shape
        if not ret:
            print("Failed to grab frame")
            break

        # Convert frame to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance
        image.flags.writeable = False
        results = face_detection.process(image)

        # Draw face detections
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
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
                print('left:',(l_ear_y-l_eye_y)*h)
                print('right:',(r_ear_y-r_eye_y)*h)
        # Display the result
        cv2.imshow('MediaPipe Face Detection', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Press 'Esc' to quit
            break

cap.release()
cv2.destroyAllWindows()
