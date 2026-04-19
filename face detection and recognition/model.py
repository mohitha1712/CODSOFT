import cv2
import numpy as np

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Face Detection
def detect_faces(image, scale=1.2, neighbors=7):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=scale,
        minNeighbors=neighbors,
        minSize=(60, 60)   # ignore very small detections
    )

    filtered_faces = []

    for (x, y, w, h) in faces:
        aspect_ratio = w / float(h)

        # ✅ Keep only near-square shapes (real faces)
        if 0.75 < aspect_ratio < 1.3:
            filtered_faces.append((x, y, w, h))

    return filtered_faces


# Draw Faces 
def draw_faces(image, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
    return image


# Blur Faces
def blur_faces(image, faces):
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.GaussianBlur(face, (99, 99), 30)
        image[y:y+h, x:x+w] = face
    return image


# Count Faces
def count_faces(faces):
    return len(faces)


# Crop Faces
def crop_faces(image, faces):
    cropped = []
    for (x, y, w, h) in faces:
        cropped.append(image[y:y+h, x:x+w])
    return cropped