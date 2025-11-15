from PIL import Image
import numpy as np

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