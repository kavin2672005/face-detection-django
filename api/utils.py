# api/utils.py
import cv2
import os
from django.conf import settings

def detect_faces(image_path, blur=False):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unreadable: " + image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Process each detected face
    face_data = []
    for (x, y, w, h) in faces:
        if blur:
            roi = img[y:y+h, x:x+w]
            roi = cv2.GaussianBlur(roi, (99, 99), 30)
            img[y:y+h, x:x+w] = roi

        # Save face metadata
        face_data.append({"x": x, "y": y, "width": w, "height": h})

        # Draw bounding box
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Create output file path (outputs folder)
    output_path = image_path.replace("uploads", "outputs")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)

    # Convert Path object to string if needed and clean the URL
    media_root_str = str(settings.MEDIA_ROOT)
    return output_path.replace(media_root_str, ''), face_data
