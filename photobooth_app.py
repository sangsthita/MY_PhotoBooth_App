import streamlit as st
import cv2
import numpy as np
from PIL import Image
import tempfile
import os

st.set_page_config(layout="centered")
st.title("📸 Streamlit AI-Powered PhotoBooth")

# Fallback method to load Haar cascade for face detection
cascade_path = os.path.join(cv2.__file__.replace('cv2.cpython-<version>.so', ''), 'data', 'haarcascades', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade_path)

# Load overlay image (heart)
heart_overlay = cv2.imread("heart.png", cv2.IMREAD_UNCHANGED)  # Add transparent heart.png in the same folder

def overlay_heart_above_head(frame, x, y, w, h):
    heart_resized = cv2.resize(heart_overlay, (w, int(h * 0.5)))
    y1 = max(y - int(h * 0.6), 0)
    y2 = y1 + heart_resized.shape[0]
    x1 = x
    x2 = x1 + heart_resized.shape[1]

    if y2 > frame.shape[0] or x2 > frame.shape[1]:
        return frame

    for i in range(heart_resized.shape[0]):
        for j in range(heart_resized.shape[1]):
            if y1 + i < frame.shape[0] and x1 + j < frame.shape[1]:
                alpha = heart_resized[i, j, 3] / 255.0
                for c in range(3):
                    frame[y1 + i, x1 + j, c] = (
                        alpha * heart_resized[i, j, c] +
                        (1 - alpha) * frame[y1 + i, x1 + j, c]
                    )
    return frame

# Sidebar filter options
filter_option = st.sidebar.selectbox("Choose a filter:", ("None", "Grayscale", "Blur", "Heart Above Head"))

# Placeholder for captured image
captured_image = None

if st.button("📷 Capture Photo from Webcam"):
    cap = cv2.VideoCapture(0)
    st.info("Press 's' to save photo or 'q' to quit camera window")

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to access camera.")
            break

        cv2.imshow("Live PhotoBooth - Press 's' to Capture, 'q' to Quit", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            img_path = os.path.join(tempfile.gettempdir(), "captured_photo.jpg")
            cv2.imwrite(img_path, frame)
            cap.release()
            cv2.destroyAllWindows()
            captured_image = img_path
            break

        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if captured_image:
    img = cv2.imread(captured_image)
    st.subheader("📸 Captured Image")

    # Face detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Apply selected filter
    if filter_option == "Grayscale":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif filter_option == "Blur":
        img = cv2.GaussianBlur(img, (15, 15), 0)
    elif filter_option == "Heart Above Head":
        for (x, y, w, h) in faces:
            img = overlay_heart_above_head(img, x, y, w, h)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Convert to PIL image for display
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    st.image(img_pil, caption=f"Detected {len(faces)} Face(s)", use_column_width=True)

    # Download link
    st.download_button("💾 Download Image", data=cv2.imencode('.jpg', cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR))[1].tobytes(), file_name="filtered_photo.jpg")

    # Expression analysis mock (for simplicity, placeholder)
    st.subheader("🧠 Expression Analysis (Mock)")
    if len(faces) == 0:
        st.write("No face detected.")
    elif len(faces) == 1:
        st.write("Expression: 😀 Likely Happy (placeholder)")
    else:
        st.write("Multiple faces detected. Group expression: 😊 Positive (placeholder)")




