from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import streamlit as st

# Load model (cached)
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    
    # Set device (GPU if available)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    return processor, model, device

processor, model, device = load_model()

# Caption generation function
def generate_caption(image):
    # Convert image to RGB (important fix)
    image = image.convert("RGB")

    # Preprocess
    inputs = processor(images=image, return_tensors="pt").to(device)

    # Generate caption (optimized)
    output = model.generate(
        **inputs,
        max_new_tokens=50,      # Fix warning + better length
        num_beams=5,            # Better quality
        early_stopping=True
    )

    # Decode
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption