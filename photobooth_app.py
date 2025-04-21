import streamlit as st
import numpy as np
import face_recognition
from PIL import Image
import os

# Set up save directory for photos
SAVE_DIR = "photos"
os.makedirs(SAVE_DIR, exist_ok=True)

# Function to add overlay (e.g., sunglasses)
def add_overlay(image, overlay_path, face_landmarks):
    overlay = Image.open(overlay_path).convert("RGBA")
    
    # Extract face coordinates
    (left, top, right, bottom) = face_landmarks
    
    # Resize overlay to fit the face
    overlay = overlay.resize((right-left, bottom-top))
    
    # Paste overlay on top of the face
    image.paste(overlay, (left, top), overlay)
    return image

# Streamlit layout
st.title("Streamlit Photobooth App 🎉")

# Use Streamlit's camera input for real-time face detection
camera_input = st.camera_input("Capture Image")

if camera_input is not None:
    # Convert captured image to PIL image
    image = Image.open(camera_input)
    st.image(image, caption="Captured Image", use_column_width=True)
    
    # Convert the image to numpy array for face recognition
    img_array = np.array(image)
    
    # Detect faces in the image using face_recognition
    face_locations = face_recognition.face_locations(img_array)
    face_landmarks = face_recognition.face_landmarks(img_array)
    
    if len(face_locations) > 0:
        st.write(f"Detected {len(face_locations)} face(s)!")
        
        # Show the image with face locations marked
        img_with_faces = img_array.copy()
        
        for face_location in face_locations:
            top, right, bottom, left = face_location
            # Draw rectangles to mark faces (no cv2, just numpy)
            img_with_faces[top:bottom, left:right] = [0, 255, 0]
        
        st.image(img_with_faces, caption="Face Detected", use_column_width=True)
        
        # Apply filters/overlay (e.g., sunglasses)
        filter_choice = st.selectbox("Choose a filter", ["None", "Sunglasses", "Hat"])
        
        if filter_choice == "Hat":
            overlay_path = "'/Users/sangsthitapanda/Desktop/Photobooth App/hat.png'"  # Update with actual path
        elif filter_choice == "Heart":
            overlay_path = "'/Users/sangsthitapanda/Desktop/Photobooth App/heart.png'"  # Update with actual path
        else:
            overlay_path = None
        
        if overlay_path:
            img_with_overlay = Image.fromarray(img_array)
            img_with_overlay = add_overlay(img_with_overlay, overlay_path, face_locations[0])
            st.image(img_with_overlay, caption="Filtered Image", use_column_width=True)
        
        # Mirror the image
        if st.checkbox("Mirror Image"):
            mirrored_image = img_array[:, ::-1]
            st.image(mirrored_image, caption="Mirrored Image", use_column_width=True)
        
        # Save photo
        if st.button("Save Photo"):
            save_path = os.path.join(SAVE_DIR, "photo.jpg")
            img_with_overlay.save(save_path)
            st.success(f"Photo saved as {save_path}")
    else:
        st.write("No faces detected. Please try again!")






