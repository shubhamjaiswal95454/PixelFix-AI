import streamlit as st
import os
import shutil
from PIL import Image
from pathlib import Path
import subprocess

st.set_page_config(page_title="PixelFix AI", layout="centered")
st.title("🖼️ PixelFix AI – Restore Old Family Photos")
st.markdown("Upload an old or damaged photo, and we'll restore or colorize it using AI models like GFPGAN and DeOldify.")

INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

uploaded_file = st.file_uploader("📷 Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    input_path = INPUT_DIR / uploaded_file.name
    output_path = OUTPUT_DIR / f"restored_{uploaded_file.name}"
    image.save(input_path)

    option = st.radio("Choose enhancement", ["🧑‍🦳 Face Restoration", "🎨 Colorization"])

    if st.button("✨ Enhance"):
        with st.spinner("Running AI model..."):
            if option == "🧑‍🦳 Face Restoration":
                # Example: Run GFPGAN
                subprocess.run(f"python gfpgan/inference_gfpgan.py -i {input_path} -o {OUTPUT_DIR} -v 1.3 --suffix restored", shell=True)
            elif option == "🎨 Colorization":
                # Placeholder for DeOldify
                subprocess.run(f"echo 'Colorization logic goes here'", shell=True)

        st.success("Done!")
        if output_path.exists():
            st.image(output_path, caption="Enhanced Image", use_column_width=True)
            with open(output_path, "rb") as file:
                st.download_button(label="📥 Download Result", data=file, file_name=output_path.name, mime="image/jpeg")
