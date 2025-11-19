import streamlit as st
from PIL import Image
import io

def display_images_side_by_side(original, processed, title1="Original", title2="Procesada"):
    """Display two images side by side."""
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"### {title1}")
        st.image(original, use_column_width=True)
    with col2:
        st.write(f"### {title2}")
        st.image(processed, use_column_width=True)

def show_spinner(text="Procesando..."):
    """Show a spinner."""
    return st.spinner(text)

def show_success(message="¡Éxito!"):
    """Show success message."""
    st.success(message)

def show_error(message="Error"):
    """Show error message."""
    st.error(message)

def create_download_button(image, filename="imagen.jpg", label="Descargar"):
    """Create download button for image."""
    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    buf.seek(0)
    st.download_button(label=label, data=buf, file_name=filename, mime="image/jpeg")

def display_metadata(metadata_dict):
    """Display metadata in a nice format."""
    for key, value in metadata_dict.items():
        st.write(f"**{key}:** {value}")

def log_message(message):
    """Log a message in the app."""
    st.write(f"🔍 {message}")