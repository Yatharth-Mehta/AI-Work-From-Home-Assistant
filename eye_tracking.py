import time
import cv2
import mediapipe as mp
import ctypes

camera = cv2.VideoCapture(0)
faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
flag = 1
alert = False
distracted_time = None

while True:
    ret, frame = camera.read()
    frame = cv2.flip(frame,1)
    rgbframe = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape
    results = faceMesh.process(rgbframe)
    landmark_points = results.multi_face_landmarks
    

    #         x = int(landmark.x * frame_width)
    #         y = int(landmark.y * frame_height)
    #         print(x,y)
    #         cv2.circle(frame,(x,y),2,(0,0,255),-1)

    if landmark_points :
        for face_landmarks in landmark_points:
        
            right_eye_x_axis = int((face_landmarks.landmark[474].x + face_landmarks.landmark[475].x + face_landmarks.landmark[476].x + face_landmarks.landmark[477].x) / 4 * frame_width)
            right_eye_y_axis = int((face_landmarks.landmark[474].y + face_landmarks.landmark[475].y + face_landmarks.landmark[476].y + face_landmarks.landmark[477].y) / 4 * frame_height)
            left_eye_x_axis = int((face_landmarks.landmark[469].x + face_landmarks.landmark[470].x + face_landmarks.landmark[471].x + face_landmarks.landmark[472].x) / 4 * frame_width)
            left_eye_y_axis = int((face_landmarks.landmark[469].y + face_landmarks.landmark[470].y + face_landmarks.landmark[471].y + face_landmarks.landmark[472].y) / 4 * frame_height)

            # right_eye_boundary_left_side = face_landmarks.landmark[469]
            # right_eye_boundary_right_side = face_landmarks.landmark[471]
            # left_eye_boundary_left_side = face_landmarks.landmark[472]
            # left_eye_boundary_right_side = face_landmarks.landmark[470]
            
            cv2.circle(frame, (right_eye_x_axis, right_eye_y_axis), 3, (0, 255, 0), -1)  
            cv2.circle(frame, (left_eye_x_axis, left_eye_y_axis), 3, (0, 255, 0), -1)
            
            
            
            
            
            
            
            right_eye_top = int(face_landmarks.landmark[475].y * frame_height)
            right_eye_bottom = int(face_landmarks.landmark[477].y * frame_height)
            right_eye_center_y = right_eye_y_axis 

            left_eye_top = int(face_landmarks.landmark[470].y * frame_height)
            left_eye_bottom = int(face_landmarks.landmark[472].y * frame_height)
            left_eye_center_y = left_eye_y_axis

            # right_center_top = right_eye_center_y - right_eye_top
            # right_center_bottom = right_eye_bottom - right_eye_center_y 
            # left_center_top = left_eye_center_y - left_eye_top
            # left_center_bottom = left_eye_bottom - left_eye_center_y
            





            
            r1 = right_eye_center_y - right_eye_top
            r2 = right_eye_bottom - right_eye_center_y 
            l1 = left_eye_center_y - left_eye_top
            l2 = left_eye_bottom - left_eye_center_y   
            if (r1 < 6.2 or r2 < 6.2 or l1 < 6.2 or l2 < 6.2):
                flag = 0
                cv2.putText(frame, "DISTRACTED", (50, 100),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)

                if distracted_time is None:
                    distracted_time = time.time() 
                else:
                    if time.time() - distracted_time > 5 and not alert:
                        ctypes.windll.user32.MessageBoxW(0, "You are distracted for more than 10 seconds!", "Alert", 0x40 | 0x1)
                        alert = True
            else:
                flag = 1
                distracted_time = None
                alert = False






    cv2.imshow('video frame', frame)
    cv2.waitKey(1)
