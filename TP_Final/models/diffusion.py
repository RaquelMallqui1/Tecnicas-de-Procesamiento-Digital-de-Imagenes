# import io
# from PIL import Image
# import numpy as np
# import cv2
# from PIL import Image, ImageEnhance
# # No importamos replicate global, usamos el client pasado por argumento

# def procesar_imagen(imagen_buffer, client, tono_piel=0.5, ropa_color=(80, 80, 150)):
#     """
#     Flujo principal de restauración optimizado.
#     Recibe: imagen_buffer (BytesIO ya saneado en app.py)
#     """
#     # 1. Cargar imagen desde el buffer limpio
#     # Usamos el buffer directamente, no intentamos hacer getvalue() si ya es BytesIO
#     try:
#         image = Image.open(imagen_buffer).convert("RGB")
#     except:
#         # Fallback por si llega un objeto UploadedFile en vez de BytesIO
#         imagen_buffer.seek(0)
#         image = Image.open(io.BytesIO(imagen_buffer.getvalue())).convert("RGB")
    
#     image = image.convert("L").convert("RGB")
#     image = restore_general_defects(image, client)

#     # 2. Restauración de Rostros y Calidad (GFPGAN)
#     # Hacemos esto PRIMERO para limpiar el ruido antes de colorear
#     image = restore_with_gfpgan(image, client)
    
#     # 3. Colorización (DeOldify)
#     image = colorize_with_deoldify(image, client)
    
#     # 4. Post-procesamiento local (OpenCV)
#     #bg_mask = mask_background(image)
#     #image = whiten_background(image, bg_mask)
#     # skin_mask = detect_skin(image)
#     # clothing_mask = detect_clothing(image, skin_mask)
    
#     # skin_color = (int(255 * tono_piel), int(200 * tono_piel), int(150 * tono_piel))
#     # image = apply_color_overlay(image, skin_mask, skin_color, 0.35)
#     # image = apply_color_overlay(image, clothing_mask, ropa_color, 0.2)
#     # Aumentar Saturación (Vida)
#     converter = ImageEnhance.Color(image)
#     image = converter.enhance(1.4) # Un 40% más de color es lo que da ese look vibrante

#     # Aumentar Contraste (Profundidad)
#     converter = ImageEnhance.Contrast(image)
#     image = converter.enhance(1.2)

#     # Ajuste de Nitidez final
#     converter = ImageEnhance.Sharpness(image)
#     image = converter.enhance(1.1)

#     return image

# def restore_with_gfpgan(image, client):
#     """Restaura definición usando GFPGAN via Replicate Client"""
#     buf = io.BytesIO()
#     image.save(buf, format='JPEG', quality=95)
#     buf.seek(0)
    
#     try:
#         # Usamos client.run, no replicate.run global
#         output = client.run(
#             "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
#             input={
#                 "img": buf,  # GFPGAN usa 'img', no 'image'
#                 "scale": 2,  # Mantenemos escala baja para evitar error 500
#                 "version": "v1.4"
#             }
#         )
#         # output suele ser una URL o un objeto file-like
#         if isinstance(output, str):
#             import requests
#             res = requests.get(output)
#             return Image.open(io.BytesIO(res.content))
#         else:
#             return Image.open(io.BytesIO(output.read()))
            
#     except Exception as e:
#         print(f"⚠️ Falló GFPGAN, continuando con imagen original: {e}")
#         return image

# def restore_general_defects(image, client):
#     """Restaura rasguños, ruido y defectos generales usando SwinIR (Inpaint)."""
#     buf = io.BytesIO()
#     # Guardar en PNG para no perder calidad antes del inpaint
#     image.save(buf, format='PNG') 
#     buf.seek(0)
    
#     try:
#         # Modelo para eliminar ruido y scratches (SwinIR)
#         output = client.run(
#             "jingyunliang/swinir:6099b25201c109267104b281f6d338cc681d45815340623a35205510618037a5",
#             input={
#                 "image": buf,
#                 "task": "classical_image_denoising" # Tarea de eliminación de ruido y defectos
#             }
#         )
        
#         if isinstance(output, str):
#             import requests
#             res = requests.get(output)
#             return Image.open(io.BytesIO(res.content))
#         else:
#             return Image.open(io.BytesIO(output.read()))
            
#     except Exception as e:
#         print(f"⚠️ Falló SwinIR/Restauración de defectos: {e}")
#         return image


# def colorize_with_deoldify(image, client):
#     """Colorea usando DeOldify via Replicate Client"""
#     buf = io.BytesIO()
#     image.save(buf, format='JPEG')
#     buf.seek(0)
    
#     try:
#         output = client.run(
#             #"cjwbw/deoldify:1106956f5429198961b44207239119a37906d4e13f5a4e2340b1cc3c666221b4",
#             "arielreplicate/deoldify_image:0da600fab0c45a66211339f1c16b71345d22f26ef5fea3dca1bb90bb5711e950",
#             input={
#                 "image": buf,
#                 "model_name": "Artistic",
#                 "render_factor": 35 # Valor seguro para evitar 500
#             }
#         )
#         if isinstance(output, str): # Si devuelve URL
#             import requests
#             res = requests.get(output)
#             return Image.open(io.BytesIO(res.content))
#         else:
#             return Image.open(io.BytesIO(output.read()))
            
#     except Exception as e:
#         print(f"⚠️ Falló DeOldify: {e}")
#         return image

# # --- FUNCIONES DE OPENCV (MANTENIDAS IGUAL) ---
# # (Aquí van tus funciones mask_background, detect_skin, etc. 
# #  No necesitas cambiarlas, solo asegúrate de que estén indentadas correctamente)

# def apply_color_overlay(image, mask, color_rgb, intensity=0.35):
#     img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#     overlay = np.full_like(img_cv, (color_rgb[2], color_rgb[1], color_rgb[0]))
#     mask_f = (mask.astype(np.float32) / 255.0)[:, :, None]
#     blended = (img_cv * (1 - mask_f * intensity) + overlay * (mask_f * intensity)).astype(np.uint8)
#     return Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))

# def detect_skin(image):
#     img_ycrcb = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2YCrCb)
#     mask = cv2.inRange(img_ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127]))
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
#     return mask

# def detect_clothing(image, skin_mask):
#     w, h = image.size
#     mask = np.zeros((h, w), dtype=np.uint8)
#     y1, y2 = int(h * 0.4), int(h * 0.95)
#     x1, x2 = int(w * 0.15), int(w * 0.85)
#     mask[y1:y2, x1:x2] = 255

#     mask = cv2.bitwise_and(mask, cv2.bitwise_not(skin_mask))
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
#     return mask

# def whiten_background(image, bg_mask):
#     img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#     white = np.full_like(img_cv, 255)
#     mask_f = (bg_mask.astype(np.float32) / 255.0)[:, :, None]
#     blended = (img_cv * (1 - mask_f) + white * mask_f).astype(np.uint8)
#     return Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))

# def mask_background(image):
#     gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
#     _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     h, w = thr.shape
#     corners = [thr[5, 5], thr[5, w-6], thr[h-6, 5], thr[h-6, w-6]]
#     bg_is_white = sum(c > 250 for c in corners) >= 2
#     bg_mask = thr if bg_is_white else cv2.bitwise_not(thr)
#     kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
#     bg_mask = cv2.morphologyEx(bg_mask, cv2.MORPH_CLOSE, kernel)
#     bg_mask = cv2.morphologyEx(bg_mask, cv2.MORPH_OPEN, kernel)
#     return bg_mask

# def get_image_info(imagen_subida):
#     # Adaptado para leer BytesIO o UploadedFile
#     try:
#         image = Image.open(imagen_subida)
#     except:
#         imagen_subida.seek(0)
#         image = Image.open(io.BytesIO(imagen_subida.getvalue()))
        
#     w, h = image.size
#     return {
#         "Resolución": f"{w} × {h} px",
#         "Formato": image.format or "JPEG",
#         "Modo": image.mode
#     }

from PIL import Image, ImageEnhance
import io
import numpy as np
import cv2
import replicate
import os
import time
# =================================================================
# UTILIDADES AUXILIARES (Necesarias para los overlays y get_info)
# (Estas son las funciones que usábamos con OpenCV, las mantenemos)
# =================================================================

def apply_color_overlay(image, mask, color_rgb, intensity=0.35):
    """Aplica un color RGB a un área específica de la imagen (máscara)."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    overlay = np.full_like(img_cv, (color_rgb[2], color_rgb[1], color_rgb[0]))
    mask_f = (mask.astype(np.float32) / 255.0)[:, :, None]
    blended = (img_cv * (1 - mask_f * intensity) + overlay * (mask_f * intensity)).astype(np.uint8)
    return Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))

def detect_skin(image):
    """Detecta el área de la piel usando el espacio de color YCrCb."""
    img_ycrcb = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2YCrCb)
    # Rangos genéricos para detección de piel
    mask = cv2.inRange(img_ycrcb, np.array([0, 133, 77]), np.array([255, 173, 127])) 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    return mask

def detect_clothing(image, skin_mask):
    """Detecta el área general de la ropa (excluyendo la piel)."""
    w, h = image.size # CORREGIDO: w, h para PIL
    mask = np.zeros((h, w), dtype=np.uint8)
    # Área de interés aproximada (cuerpo/ropa)
    y1, y2 = int(h * 0.4), int(h * 0.95)
    x1, x2 = int(w * 0.15), int(w * 0.85)
    mask[y1:y2, x1:x2] = 255
    # Restar el área de la piel
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(skin_mask))
    return mask


# =================================================================
# FUNCIONES DE LLAMADA A LA API DE REPLICATE (La magia de la IA)
# =================================================================

def restore_general_defects(image, client):
    """Restaura rasguños, ruido y defectos generales usando SwinIR (Inpaint)."""
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    
    try:
        output = client.run(
            # Versión estable de SwinIR para limpieza
            "jingyunliang/swinir:660d922d33153019e8c263a3bba265de882e7f4f70396546b6c9c8f9d47a021a",
            input={
                "image": buf,
                "task": "classical_image_denoising"
            }
        )
        time.sleep(12) 
        import requests
        res = requests.get(output)
        return Image.open(io.BytesIO(res.content))
    except Exception as e:
        # Esto capturará el error 429 o 422
        print(f"⚠️ Falló SwinIR/Restauración de defectos: ReplicateError Details: {e}") 
        return image

def restore_with_gfpgan(image, client):
    """Restaura rostros específicos usando GFPGAN."""
    buf = io.BytesIO()
    image.save(buf, format='JPEG', quality=95)
    buf.seek(0)
    
    try:
        output = client.run(
            "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
            input={
                "img": buf,  # GFPGAN usa 'img'
                "scale": 2, 
                "version": "v1.4"
            }
        )
        time.sleep(12) 
        import requests
        res = requests.get(output)
        return Image.open(io.BytesIO(res.content))
    except Exception as e:
        print(f"⚠️ Falló GFPGAN, continuando con imagen original: ReplicateError Details: {e}")
        return image

def colorize_with_deoldify(image, client):
    """Colorea usando DeOldify en modo Artístico (Vibrante)."""
    buf = io.BytesIO()
    image.save(buf, format='JPEG')
    buf.seek(0)
    
    try:
        output = client.run(
            # Modelo DeOldify Artístico (el de la captura)
            "cjwbw/deoldify_image:0da600ab233921a865574d3b330a7dc8db8b242974a99e74afb56c55fa0871e9",
            input={
                "image": buf,
                "model_name": "Artistic", 
                "render_factor": 35 
            }
        )
        time.sleep(12) 
        import requests
        res = requests.get(output)
        return Image.open(io.BytesIO(res.content))
    except Exception as e:
        print(f"⚠️ Falló DeOldify: ReplicateError Details: {e}")
        return image

# =================================================================
# FUNCIÓN PRINCIPAL DEL PROCESO
# =================================================================

def procesar_imagen(imagen_buffer, client, tono_piel=0.5, ropa_color=(80, 80, 150)):
    """Flujo completo: Limpieza, Rostros, Color y Ajustes finales."""
    
    # 1. Cargar imagen y normalizar
    try:
        image = Image.open(imagen_buffer).convert("RGB")
    except:
        imagen_buffer.seek(0)
        image = Image.open(io.BytesIO(imagen_buffer.getvalue())).convert("RGB")
        
    # 2. IA - Restauración de Rasguños y Ruido General (SwinIR)
    image = restore_general_defects(image, client) 

    # 3. IA - Restauración de Rostros (GFPGAN)
    image = restore_with_gfpgan(image, client)
    
    # 4. IA - Colorización Artística (DeOldify)
    image = colorize_with_deoldify(image, client)
    
    # 5. POST-PROCESAMIENTO MANUAL (Overlays)
    
    # 5.1 Lógica de Tono de Piel (Interpolación Piel Clara/Oscura)
    light_skin = np.array([255, 218, 190]) 
    dark_skin = np.array([90, 55, 40])     
    r = int(light_skin[0] * (1 - tono_piel) + dark_skin[0] * tono_piel)
    g = int(light_skin[1] * (1 - tono_piel) + dark_skin[1] * tono_piel)
    b = int(light_skin[2] * (1 - tono_piel) + dark_skin[2] * tono_piel)
    skin_color = (r, g, b)
    
    # # Generar máscaras y aplicar overlays (con baja intensidad para no destruir el color de la IA)
    # skin_mask = detect_skin(image)
    # clothing_mask = detect_clothing(image, skin_mask)
    
    # # Aplicar skin_color con MUY BAJA intensidad para corregir el balance de blancos
    # image = apply_color_overlay(image, skin_mask, skin_color, intensity=0.10) 
    
    # # Aplicar color de ropa (con baja intensidad para mantener las sombras del traje)
    # image = apply_color_overlay(image, clothing_mask, ropa_color, intensity=0.15) 
    # 2. IA - Restauración de Rasguños y Ruido General (SwinIR)
    image_base_clean = restore_general_defects(image, client) 

    # 3. IA - Colorización Artística (DeOldify)
    image_colorized = colorize_with_deoldify(image_base_clean, client)
    
    # 4. IA - Restauración de Rostros (GFPGAN)
    # Llama a GFPGAN con la imagen ya coloreada para que pueda arreglar los rostros a color.
    image = restore_with_gfpgan(image_colorized, client)


    # 6. BOOSTER FINAL (Aumento de Saturación, Contraste y Nitidez)
    
    # Aumentar saturación (Vida al color): 1.4 es un aumento del 40%
    converter = ImageEnhance.Color(image)
    image = converter.enhance(1.4) 

    # Aumentar contraste (Profundidad)
    converter = ImageEnhance.Contrast(image)
    image = converter.enhance(1.2)

    # Aumentar nitidez sutilmente
    converter = ImageEnhance.Sharpness(image)
    image = converter.enhance(1.1)

    return image

def get_image_info(imagen_subida):
    # Función necesaria para app.py
    try:
        image = Image.open(imagen_subida)
    except:
        imagen_subida.seek(0)
        image = Image.open(io.BytesIO(imagen_subida.getvalue()))
        
    w, h = image.size
    return {
        "Resolución": f"{w} × {h} px",
        "Formato": image.format or "JPEG",
        "Modo": image.mode
    }