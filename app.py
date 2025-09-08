import cv2  # OpenCV for computer vision
import streamlit as st  # Streamlit for building web apps
import numpy as np  # NumPy for array operations
from PIL import Image  # PIL for image handling


# Detect faces using webcam
def camera_face_detection():
    # Load Haar Cascade pre-trained classifier
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Access webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Run face detection
        faces = face_detector.detectMultiScale(
            gray_frame,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(40, 40)
        )

        # Draw bounding boxes
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Webcam Face Detection", frame)

        # Stop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


# Detect faces from uploaded image
def image_face_detection(uploaded_file):
    img = np.array(Image.open(uploaded_file))

    # Load classifier
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = face_detector.detectMultiScale(
        gray_img,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(40, 40)
    )

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    st.image(img, channels="BGR", use_column_width=True)


# ================= Streamlit Interface =================
st.title("Real-Time Face Detection App")
st.subheader("Detect faces using your webcam or an uploaded picture.")

if st.button("Start Webcam Detection"):
    camera_face_detection()

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image_face_detection(uploaded_file)
