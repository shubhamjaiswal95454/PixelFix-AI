import streamlit as st
import os
import shutil
from PIL import Image
from pathlib import Path
import subprocess

# --- Page Config ---
st.set_page_config(page_title="PixelFix AI", layout="centered")
st.title("🖼️ PixelFix AI – Restore Old Family Photos")
st.markdown("Upload an old or damaged photo, and we'll restore or colorize it using AI models like GFPGAN and DeOldify.")

# --- Directory Setup ---
INPUT_DIR = Path("inputs")
OUTPUT_DIR = Path("outputs")
RESULT_SUFFIX = "restored"
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Upload Photo ---
uploaded_file = st.file_uploader("📷 Upload a photo", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Save uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Original Image", use_column_width=True)

    input_path = INPUT_DIR / uploaded_file.name
    base_filename = uploaded_file.name.rsplit(".", 1)[0]
    output_path = OUTPUT_DIR / f"{base_filename}_{RESULT_SUFFIX}.png"
    image.save(input_path)

    # Choose enhancement type
    option = st.radio("Choose enhancement", ["🧑‍🦳 Face Restoration", "🎨 Colorization (Coming Soon)"])

    if st.button("✨ Enhance Now"):
        with st.spinner("Running AI model..."):

            if option == "🧑‍🦳 Face Restoration":
                # Run GFPGAN
                command = f"python gfpgan/inference_gfpgan.py -i {input_path} -o {OUTPUT_DIR} -v 1.3 --suffix {RESULT_SUFFIX} --only_center_face"
                subprocess.run(command, shell=True)
            elif option == "🎨 Colorization (Coming Soon)":
                st.warning("Colorization will be added soon. Stay tuned!")

        # Show output if it exists
        if output_path.exists():
            st.success("Enhancement complete!")
            st.image(output_path, caption="✨ Restored Image", use_column_width=True)

            with open(output_path, "rb") as file:
                st.download_button(
                    label="📥 Download Result",
                    data=file,
                    file_name=output_path.name,
                    mime="image/png"
                )
        else:
            st.error("❌ Restoration failed. Please check your setup.")
