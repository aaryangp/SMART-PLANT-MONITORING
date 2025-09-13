import cv2
import requests
import time

# Blynk config
BLYNK_AUTH = '1UAuQImYGec6_TqJK_8s_d9TQwJF2kqt'
ALERT_PIN = 'V3'

def send_alert(state):
    url = f"https://blynk.cloud/external/api/update?token={BLYNK_AUTH}&{ALERT_PIN}={state}"
    try:
        requests.get(url)
    except Exception as e:
        print("Failed to send alert:", e)

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
alert_sent = False

print("[INFO] Monitoring started...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0 and not alert_sent:
        print("[ALERT] Face detected! Sending alert to Blynk.")
        send_alert(1)
        alert_sent = True

    elif len(faces) == 0 and alert_sent:
        print("[INFO] No face detected. Area clear.")
        send_alert(0)
        alert_sent = False

    # Optional: Display video with rectangle around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
