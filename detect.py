import cv2
import numpy as np
from app import app
from app import Face

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Attempt to open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Unable to open camera.")
    exit()

# Load stored faces
with app.app_context():
    stored_faces = Face.query.all()
    stored_face_gray_list = []

    for stored_face in stored_faces:
        stored_image = cv2.imread(stored_face.image_path, cv2.IMREAD_GRAYSCALE)
        stored_face_gray_list.append(cv2.resize(stored_image, (100, 100)))  # Resize for consistency

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_gray = cv2.resize(gray[y:y+h, x:x+w], (100, 100))  
        
        recognized = False
        for stored_face_gray, stored_face in zip(stored_face_gray_list, stored_faces):
            match_found = np.array_equal(face_gray, stored_face_gray)
            print(f"Match found: {match_found}, Name: {stored_face.name}")
            
            if match_found:
                recognized = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(frame, f"Name: {stored_face.name}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                break
        
        if not recognized:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Not Recognized", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow('Face Recognition', frame)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # Press 'q' or Esc to exit
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
