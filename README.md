# Face Recognition App

## Introduction
The Face Recognition App is a simple application built with Flask and OpenCV for detecting and recognizing faces. This documentation provides a guide on how to use the app.py script to manage face data and templates, and the detect.py script to perform real-time face recognition.

## Requirements

Python 3.7 or higher
Flask
OpenCV

## Installation

Clone or download the Face Recognition App repository from GitHub.
bash
Copy code
git clone https://github.com/unarinel/Face-Recognition-Project.git
Install the required Python packages using pip.
bash
Copy code
pip install -r requirements.txt
Usage

### 1. Managing Face Data and Templates with app.py
The app.py script is used to manage face data, templates, and the Flask web application.

## Starting the Flask Application
### To start the Flask application, run the following command:

### bash

Copy code
python app.py
This will start the Flask server, and you can access the application through a web browser at http://localhost:5000.

## Adding a New Face

Navigate to the home page of the application.
Click on the "Add Face" button.
Fill out the form with the required information: name, address, mobile number, email, and upload an image of the face.
Click the "Submit" button to add the new face.
Viewing Stored Faces
You can view all the stored faces by navigating to the "Faces" page. This page displays a list of all faces stored in the database.

### 2. Real-Time Face Recognition with detect.py
The detect.py script is used to perform real-time face recognition using the webcam.

### Running the Face Recognition Script
To run the face recognition script, execute the following command:

### bash
Copy code
python detect.py
This will start the webcam and display a window showing real-time face detection and recognition. If a recognized face is detected, its name will be displayed below the face rectangle.

Exiting the Face Recognition Script
You can exit the face recognition script by pressing the "q" key or the Esc key while the face recognition window is active.
