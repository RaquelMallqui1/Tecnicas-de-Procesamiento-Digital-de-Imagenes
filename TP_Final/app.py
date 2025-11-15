import streamlit as st
import yaml
from PIL import Image
import io
from models.diffusion import procesar_imagen


# Cargar configuración
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

st.title(config["app"]["title"])
st.write(config["app"]["description"])

# --- Opciones de usuario ---
st.sidebar.header("Opciones de procesamiento")

modo = st.sidebar.selectbox(
    "Modo de procesamiento",
    ["Restaurar", "Colorizar", "Restaurar + Colorizar"]
)

tono = None
if modo in ["Colorizar", "Restaurar + Colorizar"]:
    tono = st.sidebar.radio(
        "Tono de color",
        ["Claro", "Medio", "Oscuro"],
        index=1
    )

# --- Subir imagen ---
imagen_original = st.file_uploader(
    "Subí tu imagen",
    type=config['app']['supported_formats']
)

if imagen_original:
    try:
        with st.spinner("Procesando imagen..."):
            imagen_procesada = procesar_imagen(imagen_original, modo, tono)

        col1, col2 = st.columns(2)
        with col1:
            st.image(imagen_original, caption="Original", use_column_width=True)
        with col2:
            st.image(imagen_procesada, caption="Procesada", use_column_width=True)

        st.success("¡Procesamiento completo!")

    except Exception as e:
        st.error(f"Error durante el procesamiento: {str(e)}")
