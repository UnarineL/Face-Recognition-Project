import streamlit as st
import os
import subprocess
import psutil
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import cv2
import numpy as np

DATABASE_URL = "sqlite:///faces.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Face(Base):
    __tablename__ = 'faces'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    mobile_number = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    image_path = Column(String(200))  

Base.metadata.create_all(engine)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load stored faces
Session = sessionmaker(bind=engine)
session = Session()
stored_faces = session.query(Face).all()
session.close()
stored_face_gray_list = []

for stored_face in stored_faces:
    stored_image = cv2.imread(stored_face.image_path, cv2.IMREAD_GRAYSCALE)
    if stored_image is not None:  
        stored_image_resized = cv2.resize(stored_image, (100, 100))
        stored_face_gray_list.append(stored_image_resized) 
    else:
        print(f"Failed to load image: {stored_face.image_path}")

def add_face(name, address, mobile_number, email, image):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    existing_face_email = session.query(Face).filter_by(email=email).first()
    existing_face_name = session.query(Face).filter_by(name=name).first()
    
    if existing_face_email:
        st.error('Email already exists. Please use a different email address.')
        session.close()
        return False
    
    if existing_face_name:
        st.error('Name already exists. Please use a different name.')
        session.close()
        return False
    
    new_face = Face(name=name, address=address, mobile_number=mobile_number, email=email)
    session.add(new_face)
    session.commit()
    
    image_path = os.path.join('static', 'faces', f'{new_face.id}.png')
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image.read())
    new_face.image_path = image_path
    
    session.commit()
    session.close()
    return True


def get_all_faces():
    Session = sessionmaker(bind=engine)
    session = Session()
    stored_faces = session.query(Face).all()
    session.close()
    return stored_faces


st.title('Face Recognition App')

with st.form(key='add_face_form'):
    st.subheader('Add a New Face')
    name = st.text_input('Name')
    address = st.text_input('Address')
    mobile_number = st.text_input('Mobile Number')
    email = st.text_input('Email')
    image = st.file_uploader('Upload Image')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if not all([name, address, mobile_number, email, image]):
        st.error('All fields are required')
    else:
        Session = sessionmaker(bind=engine)
        session = Session()
        
        existing_face_email = session.query(Face).filter_by(email=email).first()
        existing_face_name = session.query(Face).filter_by(name=name).first()
        
        if existing_face_email:
            st.error('Email already exists. Please use a different email address.')
        elif existing_face_name:
            st.error('Name already exists. Please use a different name.')
        else:
            add_face(name, address, mobile_number, email, image)
            st.success('Face data added successfully!')
        
        session.close()

show_faces = st.checkbox('Show Faces')

if show_faces:
    st.subheader('Faces in Database')
    stored_faces = get_all_faces()
    for face in stored_faces:
        st.write(f"Name: {face.name}, Address: {face.address}, Mobile Number: {face.mobile_number}, Email: {face.email}")
        if face.image_path:
            st.image(face.image_path)
        else:
            st.write("No image available")

def is_streamlit_running():
    for proc in psutil.process_iter():
        if "streamlit" in proc.name():
            return True
    return False

if not is_streamlit_running():
    streamlit_script_path = "detect_profile.py"
    command = ["streamlit", "run", streamlit_script_path]
    subprocess.run(command)

if st.button('Face Detect'):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
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

    cap.release()
    cv2.destroyAllWindows()
