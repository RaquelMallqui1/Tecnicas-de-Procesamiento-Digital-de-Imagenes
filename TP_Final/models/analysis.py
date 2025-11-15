from PIL import Image
import numpy as np

def analizar_imagen(imagen):
    """
    Analiza la imagen procesada y devuelve información básica.
    """
    # Convert to numpy array for analysis
    img_array = np.array(imagen)

    # Basic info
    width, height = imagen.size
    mode = imagen.mode

    # Color analysis (for RGB images)
    if mode == 'RGB':
        # Calculate average color
        avg_color = np.mean(img_array, axis=(0, 1))
        avg_color = tuple(avg_color.astype(int))

        # Colorfulness metric (simple)
        rg = img_array[:, :, 0] - img_array[:, :, 1]
        yb = 0.5 * (img_array[:, :, 0] + img_array[:, :, 1]) - img_array[:, :, 2]
        colorfulness = np.sqrt(np.var(rg) + np.var(yb)) + 0.3 * np.sqrt(np.mean(rg)**2 + np.mean(yb)**2)

        analysis = f"""
        **Análisis de la Imagen Colorizada:**

        - **Dimensiones:** {width} x {height} píxeles
        - **Modo:** {mode}
        - **Color Promedio:** RGB{avg_color}
        - **Vividéz del Color:** {colorfulness:.2f} (mayor valor = más colorido)

        La imagen ha sido procesada exitosamente con colores naturales.
        """
    else:
        analysis = f"""
        **Análisis de la Imagen:**

        - **Dimensiones:** {width} x {height} píxeles
        - **Modo:** {mode}

        Nota: La imagen no está en modo RGB, análisis limitado.
        """

    return analysis