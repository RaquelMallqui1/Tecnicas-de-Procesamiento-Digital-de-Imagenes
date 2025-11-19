from transformers import CLIPProcessor, CLIPModel, ViTImageProcessor, ViTForImageClassification
import torch
from PIL import Image

# ==========================================
# 1. CARGA DE MODELOS
# ==========================================
try:
    print("⏳ Cargando CLIP...")
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    print("⏳ Cargando ViT...")
    vit_processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
    vit_model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

    print("✅ Modelos cargados.")
except Exception as e:
    print(f"❌ Error cargando modelos: {e}")


# ==========================================
# 2. ANALISIS DE SIMILITUD (CLIP)
# ==========================================
def clip_similarity(img1, img2):
    """Comparación semántica entre imágenes (0 a 1)."""
    try:
        images = [img1, img2]
        inputs = clip_processor(images=images, return_tensors="pt", padding=True)

        with torch.no_grad():
            feats = clip_model.get_image_features(**inputs)
            feats = feats / feats.norm(p=2, dim=-1, keepdim=True)

            sim = torch.nn.functional.cosine_similarity(
                feats[0].unsqueeze(0),
                feats[1].unsqueeze(0)
            ).item()

        return sim
    except Exception as e:
        print(f"⚠️ Error similitud CLIP: {e}")
        return 0.0


# ==========================================
# 3. CLASIFICACIÓN DE CALIDAD (ZERO-SHOT)
# ==========================================
def clip_quality(processed_image):
    categorias = [
        "imagen de muy alta calidad y nítida",
        "imagen restaurada y clara",
        "imagen borrosa con artefactos",
        "fotografía antigua en sepia o blanco y negro",
        "fotografía profesional con buen detalle"
    ]

    inputs = clip_processor(text=categorias, images=processed_image, return_tensors="pt", padding=True)
    
    with torch.no_grad():
        outputs = clip_model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        idx = probs.argmax().item()

    return categorias[idx], probs.max().item()


# ==========================================
# 4. CLASIFICACIÓN DE CONTENIDO (VIT)
# ==========================================
def classify_content(image):
    inputs = vit_processor(images=image.convert("RGB"), return_tensors="pt")

    with torch.no_grad():
        outputs = vit_model(**inputs)
        idx = outputs.logits.argmax(-1).item()
        label = vit_model.config.id2label[idx]

    return label


# ==========================================
# 5. DESCRIPCIÓN ZERO-SHOT (CLIP)
# ==========================================
def clip_generate_description(processed):
    opciones = [
        "a restored color photo",
        "a blurry damaged photo",
        "a high quality portrait",
        "a family photo",
        "a photo with enhanced colors and sharpness",
        "an old black and white vintage photo"
    ]

    inputs = clip_processor(text=opciones, images=processed, return_tensors="pt", padding=True)

    with torch.no_grad():
        out = clip_model(**inputs)
        idx = out.logits_per_image.softmax(dim=1).argmax().item()

    return opciones[idx]


# ==========================================
# 6. FUNCIÓN PRINCIPAL
# ==========================================
def analyze_images(original_image, processed_image):
    """Función principal unificada y final."""

    # 1. Similitud semántica
    similarity = clip_similarity(original_image, processed_image)

    # 2. Calidad
    calidad, prob = clip_quality(processed_image)

    # 3. Contenido (ViT)
    clase_original = classify_content(original_image)
    clase_procesada = classify_content(processed_image)

    # 4. Descripción
    descripcion = clip_generate_description(processed_image)

    return {
        "descripcion": descripcion,
        "similitud_semantica": f"{similarity:.2%}",
        "clase_original": clase_original,
        "clase_procesada": clase_procesada,
        "calidad_clasificada": calidad,
        "calidad_mejorada": similarity > 0.85
    }
