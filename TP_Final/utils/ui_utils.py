import streamlit as st
from PIL import Image

def mostrar_imagenes_lado_a_lado(imagen1, imagen2, caption1="Original", caption2="Procesada"):
    """
    Muestra dos imágenes lado a lado en Streamlit.
    """
    col1, col2 = st.columns(2)
    with col1:
        st.image(imagen1, caption=caption1, use_column_width=True)
    with col2:
        st.image(imagen2, caption=caption2, use_column_width=True)

def mostrar_spinner(texto="Procesando..."):
    """
    Muestra un spinner con texto personalizado.
    """
    return st.spinner(texto)

def mostrar_exito(mensaje="¡Operación completada!"):
    """
    Muestra un mensaje de éxito.
    """
    st.success(mensaje)

def mostrar_error(mensaje="Ocurrió un error."):
    """
    Muestra un mensaje de error.
    """
    st.error(mensaje)

def validar_imagen_subida(imagen, max_size_mb=5):
    """
    Valida que la imagen subida cumpla con los requisitos.
    """
    if imagen is None:
        return False, "No se ha subido ninguna imagen."

    # Check size
    size_mb = len(imagen.getvalue()) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"La imagen es demasiado grande ({size_mb:.2f} MB). Máximo {max_size_mb} MB."

    # Check format
    allowed_formats = ['jpg', 'jpeg', 'png']
    if imagen.type.split('/')[-1].lower() not in allowed_formats:
        return False, f"Formato no soportado. Use: {', '.join(allowed_formats)}."

    return True, "Imagen válida."