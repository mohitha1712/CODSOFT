# Task 5: Face Detection System

## Description
This project implements a Face Detection system using Python and OpenCV. It detects human faces in images using a pre-trained Haar Cascade classifier and provides additional functionalities such as face highlighting, blurring, cropping, and counting.

## Features
- Detects faces in images using Haar Cascade classifier
- Filters detections based on aspect ratio for improved accuracy
- Draws bounding boxes around detected faces
- Applies blur effect to detected faces
- Crops individual face regions
- Counts the number of detected faces
- Modular and reusable code structure

## Technologies Used
- Python
- OpenCV
- NumPy

## How to Run
1. Install dependencies:
   pip install -r requirements.txt

2. Make sure the Haar Cascade file is available:
   haarcascade_frontalface_default.xml

3. Run the program:
   python app.py

## Output
![Face Detection Output](output.png)

## Project Structure
face_detection/
│── app.py
│── model.py
│── requirements.txt
│── README.md
│── output.png
│── haarcascade_frontalface_default.xml


## Working Principle
The system converts the input image into grayscale and uses a pre-trained Haar Cascade classifier to detect faces. 

Detected regions are filtered based on aspect ratio to remove false positives. The final detected faces are then processed to draw bounding boxes, apply blur effects, crop face regions, or count the number of faces.

## Applications
- Image processing applications
- Privacy protection (face blurring)
- Face-based data analysis
- Preprocessing for face recognition systems