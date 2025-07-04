import ctypes
import time
import cv2
import mediapipe as mp

drawmp = mp.solutions.drawing_utils
posemp = mp.solutions.pose
video = cv2.VideoCapture(0)
flag = 1
alert = False
time_of_distraction = None



def get_difference(x,y):
    return abs(x[0]-y[0])




with posemp.Pose(min_detection_confidence = 0.6, min_tracking_confidence = 0.6) as pose :
    while video.isOpened():
        ret, frame = video.read()
        frame = cv2.flip(frame,1)
        if not ret:
            break


        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)






        try:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = [landmarks[posemp.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[posemp.PoseLandmark.LEFT_SHOULDER.value].y]
            left_ear = [landmarks[posemp.PoseLandmark.LEFT_EAR.value].x,landmarks[posemp.PoseLandmark.LEFT_EAR.value].y]

            difference = get_difference(left_ear,left_shoulder)*frame.shape[1]



            if difference > 105:
                posture = "Slouching"
                color = (0,0,255)
                flag = 0
                if time_of_distraction is None:
                    time_of_distraction = time.time() 
                else:
                    if time.time() - time_of_distraction > 5 and not alert:
                        ctypes.windll.user32.MessageBoxW(0, "The Posture is not Correct !", "Alert", 0x60 | 0x1)
                        alert = True
            else:
                posture = "Good Posture"
                color = (0,255,0)
                flag = 1
                time_of_distraction = None
                alert = False




            cv2.putText(image, f'Posture: {posture}', (30, 50),cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            cv2.putText(image, f'Ear-Shoulder Offset: {int(difference)}px', (30, 90),cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2, cv2.LINE_AA)

            drawmp.draw_landmarks(image, results.pose_landmarks, mp.POSE_CONNECTIONS)

        except:
            pass




        cv2.imshow('Posture Recognition',image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()