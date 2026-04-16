import streamlit as st
from PIL import Image
from model import generate_caption

# Page config
st.set_page_config(page_title="Image Caption Generator", page_icon="🖼️", layout="centered")

# 🎨 MODERN UI
st.markdown("""
<style>

body {
    background: linear-gradient(135deg, #1e1e2f, #0f2027);
}

.title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #00c6ff;
}

.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 30px;
}

.upload-box {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.05);
    text-align: center;
}

.caption-box {
    padding: 15px;
    border-radius: 15px;
    background: rgba(0,198,255,0.1);
    color: white;
    font-size: 18px;
}

div.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(145deg, #00c6ff, #0072ff);
    color: white;
    font-size: 16px;
    font-weight: bold;
    transition: 0.2s;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# 🎯 TITLE
st.markdown('<div class="title">🖼️ Image Caption AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload an image and let AI describe it</div>', unsafe_allow_html=True)

st.write("---")

# 📤 UPLOAD
uploaded_file = st.file_uploader("📂 Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")

        # Show image
        st.image(image, caption="📸 Uploaded Image", width=400)

        st.write("")

        if st.button("✨ Generate Caption"):
            with st.spinner("🤖 AI is analyzing..."):
                caption = generate_caption(image)

            st.success("✅ Caption Generated!")

            st.markdown("### 📝 Caption")
            st.markdown(f"<div class='caption-box'>{caption}</div>", unsafe_allow_html=True)

            st.download_button(
                label="⬇ Download Caption",
                data=caption,
                file_name="caption.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error("⚠ Error processing image")
        st.text(str(e))

else:
    st.info("👆 Upload an image to start")

st.write("---")

# Footer
st.markdown(
    "<p style='text-align:center; color:gray;'>Built using BLIP Transformer Model 🤖</p>",
    unsafe_allow_html=True
)