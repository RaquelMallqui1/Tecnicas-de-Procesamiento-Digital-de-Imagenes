import streamlit as st
import yaml
from PIL import Image
import io
from models.diffusion import procesar_imagen, get_image_info
from models.analysis import analyze_images
from utils.image_utils import calculate_ssim, calculate_psnr, extract_metadata
from utils.ui_utils import display_images_side_by_side, show_success, show_error, create_download_button, display_metadata, log_message
from utils.image_utils import sanear_imagen_para_api

import replicate
import os

# ==============================================
# 1. CARGAR TOKEN DESDE SECRETS
# ==============================================
try:
    api_token = st.secrets["replicate"]["api_token"]
except KeyError:
    st.error("❌ No se encontró 'api_token' en .streamlit/secrets.toml")
    st.stop()

# ==============================================
# 2. FORZAR TOKEN EN VARIABLE DE ENTORNO
# ==============================================
os.environ["REPLICATE_API_TOKEN"] = api_token 

# ==============================================
# 3. INICIALIZAR CLIENTE REPLICATE
# ==============================================
client = replicate.Client()

# ==============================================
# 4. CARGAR CONFIGURACIÓN
# ==============================================
try:
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
except (FileNotFoundError, yaml.YAMLError) as e:
    st.error(f"❌ Error al cargar config.yaml: {e}")
    config = {}

# ==============================================
# TITULO Y DESCRIPCIÓN
# ==============================================
st.title(config.get("app", {}).get("title", "Photo Colorization App"))
st.write(config.get("app", {}).get("description", "Revive tus recuerdos familiares"))

# ==============================================
# UPLOAD
# ==============================================
supported_formats = config.get("app", {}).get("supported_formats", ["jpg", "png", "jpeg"])
imagen_subida = st.file_uploader("Seleccioná una imagen", type=supported_formats)

if imagen_subida:
    buffer_limpio = sanear_imagen_para_api(imagen_subida)
    imagen_original = Image.open(io.BytesIO(buffer_limpio.getvalue())).convert("RGB")

    # ----------------------------------------------
    # SIDEBAR
    # ----------------------------------------------
    with st.sidebar:
        st.header("⚙ Configuración")
        default_tone = config.get("processing", {}).get("default_tone", 0.5)
        tono_piel = st.slider("Tono de piel", 0.0, 1.0, default_tone)

        default_ropa_color = config.get("processing", {}).get("default_ropa_color", [255, 255, 255])
        ropa_color = st.color_picker("Color de ropa", "#%02x%02x%02x" % tuple(default_ropa_color))
        ropa_color = tuple(int(ropa_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))

        if st.button("Procesar imagen"):
            with st.spinner("Procesando imagen..."):
                try:
                    log_message("Iniciando procesamiento...")
                    imagen_resultado = procesar_imagen(buffer_limpio, client, tono_piel, ropa_color)
                    log_message("Procesamiento completado. Analizando...")

                    # -------------------------------
                    # ANÁLISIS INTELIGENTE
                    # -------------------------------
                    analysis = analyze_images(imagen_original, imagen_resultado)
                    ssim_score = calculate_ssim(imagen_original, imagen_resultado)
                    psnr_score = calculate_psnr(imagen_original, imagen_resultado)

                    buf = io.BytesIO()
                    imagen_resultado.save(buf, format='JPEG')
                    st.session_state['imagen_procesada_bytes'] = buf.getvalue()
                    st.session_state['analysis'] = analysis
                    st.session_state['ssim'] = ssim_score
                    st.session_state['psnr'] = psnr_score
                    st.session_state['metadata_original'] = get_image_info(imagen_subida)
                    st.session_state['metadata_procesada'] = extract_metadata(imagen_resultado)

                    show_success("¡Procesado exitoso!")

                except Exception as e:
                    show_error(f"Error: {str(e)}")

# ==============================================
# MOSTRAR RESULTADOS
# ==============================================
if 'analysis' in st.session_state:

    st.subheader("🤖 Análisis Inteligente")
    analisis_data = st.session_state['analysis']

    # ---- Evaluación por IA ----
    st.markdown("### 🔍 Evaluación por la IA")
    st.write(f"**Clasificación Final:** {analisis_data['calidad_clasificada']}")
    st.info(f"**Resumen de la IA:** {analisis_data['descripcion']}")

    # ---- Análisis de Contenido ----
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Clase Contenido Original:** {analisis_data['clase_original']}")
        st.write(f"**Similitud Semántica:** {analisis_data['similitud_semantica']}")

    # ---- Métricas SSIM / PSNR ----
    st.markdown("### 📊 Métricas Cuantitativas")
    st.write(f"**SSIM:** {st.session_state['ssim']:.3f}")
    st.write(f"**PSNR:** {st.session_state['psnr']:.2f} dB")
    st.write(f"**Calidad Mejorada:** {'Sí' if analisis_data['calidad_mejorada'] else 'No'}")

    # ---- Mostrar imágenes ----
    imagen_procesada = Image.open(io.BytesIO(st.session_state['imagen_procesada_bytes']))
    st.markdown('<div class="card">', unsafe_allow_html=True)
    display_images_side_by_side(imagen_original, imagen_procesada)

    # ---- Metadatos ----
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Metadatos Original")
        display_metadata(st.session_state['metadata_original'])
    with col2:
        st.subheader("📊 Metadatos Procesada")
        display_metadata(st.session_state['metadata_procesada'])

    # ---- Download ----
    st.subheader("📥 Descargar")
    create_download_button(imagen_procesada, "imagen_procesada.jpg", "Descargar Imagen Procesada")

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================
# ESTILOS
# ==============================================
st.markdown("""
<style>
.card {
    background: white;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    margin-bottom: 24px;
}
main {
    background-color: #F4F6F9;
    max-width: 1400px;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)
