from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import cv2
import io

def sanear_imagen_para_api(imagen_file, max_size=2048):
    """
    Prepara la imagen para evitar errores 500 en Replicate:
    1. Convierte a RGB (elimina canales alfa problemáticos).
    2. Redimensiona si es demasiado grande (ahorra VRAM en el servidor).
    3. Devuelve bytes limpios.
    """
    try:
        # Abrir imagen desde el upload de Streamlit
        img = Image.open(imagen_file)
        
        # 1. Convertir a RGB (vital para evitar errores de formato)
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # 2. Redimensionar si excede el tamaño seguro (downscaling)
        # Muchos modelos crashean con lados mayores a 2000-3000px
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # 3. Guardar en buffer de memoria
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        buffer.seek(0) # Rebobinar el buffer
        
        return buffer
        
    except Exception as e:
        print(f"Error al procesar imagen localmente: {e}")
        return imagen_file # En el peor caso, devuelve el original

def comparar_imagenes(imagen1, imagen2):
    """
    Compara dos imágenes y devuelve métricas de diferencia.
    """
    # Convert to arrays
    arr1 = np.array(imagen1.convert('RGB'))
    arr2 = np.array(imagen2.convert('RGB'))

    # Ensure same size
    if arr1.shape != arr2.shape:
        # Resize second to match first
        imagen2_resized = imagen2.resize(imagen1.size)
        arr2 = np.array(imagen2_resized.convert('RGB'))

    # Mean Squared Error
    mse = np.mean((arr1 - arr2) ** 2)

    # Peak Signal-to-Noise Ratio (PSNR)
    if mse == 0:
        psnr = float('inf')
    else:
        max_pixel = 255.0
        psnr = 20 * np.log10(max_pixel / np.sqrt(mse))

    comparison = f"""
    **Comparación entre Imágenes:**

    - **Error Cuadrático Medio (MSE):** {mse:.2f}
    - **Relación Señal-Ruido (PSNR):** {psnr:.2f} dB

    Un PSNR más alto indica mayor similitud entre las imágenes.
    """

    return comparison

def redimensionar_imagen(imagen, max_size=1024):
    """
    Redimensiona la imagen si es demasiado grande.
    """
    width, height = imagen.size
    if max(width, height) > max_size:
        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)
        return imagen.resize((new_width, new_height), Image.LANCZOS)
    return imagen

def calculate_ssim(imagen1, imagen2):
    """Calculate SSIM between two images."""
    arr1 = np.array(imagen1.convert('RGB'))
    arr2 = np.array(imagen2.convert('RGB'))
    if arr1.shape != arr2.shape:
        imagen2 = imagen2.resize(imagen1.size)
        arr2 = np.array(imagen2.convert('RGB'))
    gray1 = cv2.cvtColor(arr1, cv2.COLOR_RGB2GRAY)
    gray2 = cv2.cvtColor(arr2, cv2.COLOR_RGB2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score

def calculate_psnr(imagen1, imagen2):
    """Calculate PSNR between two images."""
    arr1 = np.array(imagen1.convert('RGB'))
    arr2 = np.array(imagen2.convert('RGB'))
    if arr1.shape != arr2.shape:
        imagen2 = imagen2.resize(imagen1.size)
        arr2 = np.array(imagen2.convert('RGB'))
    return psnr(arr1, arr2)

def get_histogram(imagen):
    """Get histogram of the image."""
    arr = np.array(imagen.convert('RGB'))
    hist_r = cv2.calcHist([arr], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([arr], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([arr], [2], None, [256], [0, 256])
    return hist_r.flatten(), hist_g.flatten(), hist_b.flatten()

def extract_metadata(imagen):
    """Extract metadata from image."""
    info = imagen.info
    exif_data = info.get("exif")
    if exif_data is not None and isinstance(exif_data, bytes):
        exif_data = exif_data.hex()  # Convert bytes to hex string for JSON serialization
    return {
        "format": imagen.format,
        "mode": imagen.mode,
        "size": list(imagen.size),  # Convert tuple to list for JSON serialization
        "exif": exif_data
    }