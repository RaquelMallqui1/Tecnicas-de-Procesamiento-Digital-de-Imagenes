from PIL import Image, ImageEnhance, ImageFilter
import io

def restaurar_imagen(image):
    """Aplica una restauración suave a la imagen."""
    # Reducción de ruido
    restored = image.filter(ImageFilter.MedianFilter(size=3))

    # Aumento ligero de nitidez
    restored = restored.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))

    # Mejorar contraste
    contrast = ImageEnhance.Contrast(restored).enhance(1.2)

    # Mejorar brillo
    bright = ImageEnhance.Brightness(contrast).enhance(1.05)

    return bright


def colorizar_imagen(image, tono="Medio"):
    """Coloriza la imagen según el tono elegido."""
    # Pasar a escala de grises
    gray = image.convert("L")

    # Mejorar contraste
    enhanced = ImageEnhance.Contrast(gray).enhance(1.4)

    # Suavizar ruido
    smoothed = enhanced.filter(ImageFilter.SMOOTH)

    # Tonos predefinidos
    tonos = {
        "Claro": (210, 170, 140),
        "Medio": (160, 120, 90),
        "Oscuro": (110, 80, 60)
    }

    color_overlay = Image.new("RGB", image.size, tonos.get(tono, tonos["Medio"]))

    # Convertimos gris a RGB para mezclar
    base = Image.merge("RGB", (smoothed, smoothed, smoothed))

    # Mezcla final
    colorized = Image.blend(base, color_overlay, 0.35)

    # Pequeña mejora de brillo
    final = ImageEnhance.Brightness(colorized).enhance(1.05)

    return final


def procesar_imagen(imagen_original, modo="Colorizar", tono="Medio"):
    """Procesa la imagen según el modo elegido."""
    # Convertir archivo subido en PIL
    image = Image.open(io.BytesIO(imagen_original.getvalue()))

    # Seleccionar acción
    if modo == "Restaurar":
        return restaurar_imagen(image)

    elif modo == "Colorizar":
        return colorizar_imagen(image, tono)

    elif modo == "Restaurar + Colorizar":
        restored = restaurar_imagen(image)
        return colorizar_imagen(restored, tono)

    return image
