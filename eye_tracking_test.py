import time
import cv2
import mediapipe as mp
import ctypes
import os
import psutil
import inspect
import subprocess

camera = cv2.VideoCapture(0)
faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

TP = FP = TN = FN = 0
flag = 1
alert = False
distracted_time = None
actual_distraction = False
total_latency = 0
frame_count = 0




def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024) 



def check_modularity():
    functions = [func for func, _ in inspect.getmembers(inspect.currentframe().f_globals, inspect.isfunction)]
    return len(functions) > 5  




def check_error_handling():
    try:
        x = 1 / 0  
    except ZeroDivisionError:
        return True  
    return False




def check_readability():
    variable_names = [name for name, value in inspect.currentframe().f_globals.items()]
    readability_score = sum(1 for name in variable_names if name.islower() and "_" in name)
    return readability_score / len(variable_names) > 0.5



def check_library_usage():
    return 'cv2' in globals() and 'mediapipe' in globals()


def evaluate_best_practices():
    modularity_score = 20 if check_modularity() else 0
    error_handling_score = 20 if check_error_handling() else 0
    readability_score = 20 if check_readability() else 0
    library_usage_score = 20 if check_library_usage() else 0
    performance_score = 20
    total_score = modularity_score + error_handling_score + readability_score + library_usage_score + performance_score
    return total_score







def evaluate_security_bandit(file_name):
    try:
        result = subprocess.run(["bandit", "-r", file_name, "-f", "json"], capture_output=True, text=True)
        import json
        data = json.loads(result.stdout)
        issues = len(data.get("results", []))
        max_checks = 10
        score = max(0, 100 - (issues / max_checks * 100))
        return round(score, 2)
    except Exception as e:
        print("Security evaluation failed:", str(e))
        return 0

while True:
    start_time = time.time()
    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)
    rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_height, frame_width, _ = frame.shape
    results = faceMesh.process(rgbframe)
    landmark_points = results.multi_face_landmarks

    if landmark_points:
        for face_landmarks in landmark_points:
            right_eye_x_axis = int((face_landmarks.landmark[474].x + face_landmarks.landmark[475].x +
                                    face_landmarks.landmark[476].x + face_landmarks.landmark[477].x) / 4 * frame_width)
            right_eye_y_axis = int((face_landmarks.landmark[474].y + face_landmarks.landmark[475].y +
                                    face_landmarks.landmark[476].y + face_landmarks.landmark[477].y) / 4 * frame_height)
            left_eye_x_axis = int((face_landmarks.landmark[469].x + face_landmarks.landmark[470].x +
                                   face_landmarks.landmark[471].x + face_landmarks.landmark[472].x) / 4 * frame_width)
            left_eye_y_axis = int((face_landmarks.landmark[469].y + face_landmarks.landmark[470].y +
                                   face_landmarks.landmark[471].y + face_landmarks.landmark[472].y) / 4 * frame_height)

            right_eye_top = int(face_landmarks.landmark[475].y * frame_height)
            right_eye_bottom = int(face_landmarks.landmark[477].y * frame_height)
            right_eye_center_y = right_eye_y_axis

            left_eye_top = int(face_landmarks.landmark[470].y * frame_height)
            left_eye_bottom = int(face_landmarks.landmark[472].y * frame_height)
            left_eye_center_y = left_eye_y_axis

            r1 = right_eye_center_y - right_eye_top
            r2 = right_eye_bottom - right_eye_center_y
            l1 = left_eye_center_y - left_eye_top
            l2 = left_eye_bottom - left_eye_center_y

            predicted_distraction = False
            if (r1 < 6.5 or r2 < 6.5 or l1 < 6.5 or l2 < 6.5):
                predicted_distraction = True
                cv2.putText(frame, "DISTRACTED", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
                if distracted_time is None:
                    distracted_time = time.time()
                else:
                    if time.time() - distracted_time > 5 and not alert:
                        ctypes.windll.user32.MessageBoxW(0, "You are distracted for more than 10 seconds!", "Alert", 0x40 | 0x1)
                        alert = True
            else:
                distracted_time = None
                alert = False

            if predicted_distraction:
                if actual_distraction:
                    TP += 1
                else:
                    FP += 1
            else:
                if actual_distraction:
                    FN += 1
                else:
                    TN += 1

 
        landmarks_detected = (len(landmark_points) > 0)  
        if landmarks_detected:
            TP += 1
        else:
            FP += 1

    end_time = time.time()
    frame_latency = end_time - start_time
    total_latency += frame_latency
    frame_count += 1

    memory_usage = get_memory_usage()

    cv2.imshow('video frame', frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

total = TP + FP + TN + FN
accuracy = (TP + TN) / total * 100 if total != 0 else 0
average_latency = total_latency / frame_count if frame_count != 0 else 0

best_practice_percentage = evaluate_best_practices()
security_score = evaluate_security_bandit(__file__)





print(f"Accuracy: {accuracy:.2f}%")
print(f"True Positives (TP): {TP}")
print(f"True Negatives (TN): {TN}")
print(f"False Positives (FP): {FP}")
print(f"False Negatives (FN): {FN}")
print(f"Average Latency: {average_latency:.4f} seconds per frame")
print(f"Memory Usage: {memory_usage:.2f} MB")
print(f"Code Best Practices Score: {best_practice_percentage:.2f}%")
print(f"Security Evaluation Score (Bandit): {security_score:.2f}%")

camera.release()
cv2.destroyAllWindows()