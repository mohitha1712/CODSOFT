import streamlit as st
import cv2
import numpy as np
from model import detect_faces, draw_faces, blur_faces, crop_faces, count_faces

st.set_page_config(page_title="AI Face Detection System")

st.title("AI Face Detection & Privacy Analysis System")

# Upload
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# Mode selection
mode = st.selectbox(
    "Select Feature",
    ["Face Detection", "Face Blur (Privacy)", "Face Count", "Face Extraction"]
)

# Sidebar controls
st.sidebar.header("Advanced Settings")
scale = st.sidebar.slider("Scale Factor", 1.05, 1.3, 1.15)
neighbors = st.sidebar.slider("Min Neighbors", 6, 12, 9)

# Processing
if uploaded_file is not None:

    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    # Detect faces
    faces = detect_faces(image, scale, neighbors)

    st.subheader("Analysis Results")

    col1, col2 = st.columns(2)

    # LEFT: Original Image
    with col1:
        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
                 caption="Original Image",
                 width="stretch")

    # RIGHT: Output
    with col2:

        if mode == "Face Detection":
            result = draw_faces(image.copy(), faces)
            st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB),
                     caption="Detected Faces",
                     width="stretch")

        elif mode == "Face Blur (Privacy)":
            result = blur_faces(image.copy(), faces)
            st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB),
                     caption="Blurred Faces",
                     width="stretch")

        elif mode == "Face Count":
            count = count_faces(faces)
            st.metric(label="Faces Detected", value=count)

            result = draw_faces(image.copy(), faces)
            st.image(cv2.cvtColor(result, cv2.COLOR_BGR2RGB),
                     caption="Detection Result",
                     width="stretch")

        elif mode == "Face Extraction":
            cropped = crop_faces(image, faces)

            if len(cropped) == 0:
                st.warning("No faces detected")
            else:
                st.write("Extracted Faces:")
                for i, face in enumerate(cropped):
                    st.image(cv2.cvtColor(face, cv2.COLOR_BGR2RGB),
                             caption="Face " + str(i+1),
                             width=150)

    # Download processed image
    if 'result' in locals():
        _, buffer = cv2.imencode('.jpg', result)
        st.download_button(
            label="Download Processed Image",
            data=buffer.tobytes(),
            file_name="output.jpg",
            mime="image/jpeg"
        )