import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

def validate_image(img_file):
    """Check if the uploaded file is a valid image."""
    try:
        # Validate image using PIL
        with Image.open(img_file) as img:
            img.verify()  # Verify that this is an image
        img_file.seek(0)  # Reset the file pointer for future reads
        return True
    except Exception as e:
        st.error(f"Uploaded file is not a valid image: {e}")
        return False

def process_image(img_file):
    """Remove the background from an image."""
    try:
        # Read image data
        image_data = img_file.getvalue()  # Using getvalue to ensure we read the full content

        # Use rembg to remove the background
        result_data = remove(image_data)

        if result_data:
            # Convert bytes result back to a PIL image for display
            result_image = Image.open(BytesIO(result_data))
            return result_image.convert('RGBA')  # Convert to RGBA to ensure transparency handling
        else:
            st.error("Failed to remove background - no output from rembg.")
            return None
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

# Streamlit interface
st.title("Background Removal Tool")
st.write("Upload an image and remove its background with a single click.")

uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

if uploaded_file:
    if validate_image(uploaded_file):
        original_image = Image.open(uploaded_file)
        # Use columns to display images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="Original Image", use_column_width=True)
            # Place the remove background button below the original image
            if st.button("Remove Background"):
                with st.spinner("Processing..."):
                    result_image = process_image(uploaded_file)
                    if result_image:
                        # Display the processed image in the second column after processing
                        with col2:
                            st.image(result_image, caption="Image without Background", use_column_width=True)
                            # Save to bytes buffer
                            buf = BytesIO()
                            result_image.save(buf, format="PNG")
                            # Place the download button right below the processed image
                            st.download_button(label="Download Result", data=buf.getvalue(), file_name="no_bg.png", mime="image/png")
    else:
        st.error("Please upload a valid image file.")
else:
    st.info("Awaiting image upload.")
