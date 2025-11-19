# 🖼️ Sistema de Restauración y Colorización Fotográfica con IA

> **MVP (Producto Mínimo Viable) diseñado para restaurar, colorear y analizar la calidad de fotografías antiguas mediante un pipeline que integra modelos de difusión.**

---

## 🌟 1. El Problema y la Solución (MVP)

### Problema Core

Las fotografías familiares escaneadas de décadas pasadas están degradadas, tienen rasguños, carecen de nitidez y presentan un tinte sepia que disminuye su valor emocional y visual. Las herramientas de edición convencionales son complejas y no pueden reconstruir los detalles faciales perdidos.

### Solución: Sistema Inteligente de Recuperación de Imagenes

Este sistema automatiza el proceso de restauración en tres fases principales:
1.  **Limpieza y Super-resolución:** Elimina ruido y aumenta la nitidez de los rostros (GFPGAN / SwinIR).
2.  **Colorización Artística:** Añade colores vibrantes y naturales (DeOldify Artistic).
3.  **Análisis Inteligente:** Evalúa la calidad de la restauración en lenguaje natural (CLIP/ViT).

## 👩‍🦰 2. User Persona (Diseño Centrado en el Usuario)

Todas las decisiones de diseño del MVP están orientadas a las necesidades de esta persona:

| Característica | Detalle |
| :--- | :--- |
| **Nombre** | **Laura, la Fotógrafa Amateur** |
| **Problema** | "Tengo cientos de fotos familiares escaneadas que se ven pixeladas y opacas." |
| **Frustración** | Las herramientas complejas o de suscripción no ofrecen resultados consistentes. |
| **Objetivo** | Obtener una versión nítida y a color de sus fotos antiguas de forma **simple** y **rápida**. |

---

## 📐 3. Arquitectura del Sistema

El proyecto sigue el **Track 1: Recuperación de Imágenes** y utiliza un pipeline secuencial de múltiples modelos de IA (APIs) para lograr el resultado final.

### Stack Tecnológico

| Componente | Tecnología | Rol Principal |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit | Interfaz interactiva y gestión del flujo. |
| **Procesamiento Difusión** | Replicate API (SwinIR, GFPGAN, DeOldify) | Ejecuta el procesamiento pesado en la nube. |
| **Análisis Visual** | Hugging Face Transformers (CLIP, ViT) | Clasificación de calidad y contenido (Ejecución Local/CPU). |
| **Manipulación** | PIL/Pillow y OpenCV | Pre-saneamiento, generación de máscaras y ajustes finales. |

### Flujo de Datos (Pipeline)

[USUARIO] → [Streamlit UI] → [SwinIR (Limpieza)] → [GFPGAN (Rostros)] → [DeOldify (Color)] → [Análisis (CLIP/ViT)] → [Resultados UI]

---

## 🧠 4. Decisiones de Diseño (Human-AI Interaction - HAI)

### Transparencia y Feedback
* **Decisión:** Uso de mensajes `st.spinner` y `log_message` que indican la etapa (`Procesando Rostros...`, `Analizando...`).
* **Justificación:** El procesamiento es lento y ocurre en la nube (API). El usuario necesita **feedback constante** para entender que el sistema está trabajando.

### Control y Explicabilidad
* **Decisión:** El resultado del Análisis Visual se presenta con titulares en **lenguaje humano** (`Clasificación Final`, `Resumen de la IA`) junto con métricas técnicas (`SSIM`, `PSNR`).
* **Justificación:** El análisis con CLIP/ViT traduce el éxito técnico en un mensaje comprensible y de valor para el usuario.

### Manejo de Errores (Contingencia)
* **Decisión:** Implementación de bloques `try...except` que devuelven la imagen original y muestran un `st.error()` si la API falla por cuota (`402`) o límite de tasa (`429`).
* **Justificación:** Evita que la aplicación se rompa y comunica el error al usuario de manera clara ("Error de infraestructura, intenta en unos segundos").

---

## 5. 🔬 Conceptos de Procesamiento Digital Aplicados

El proyecto aplica varios conceptos fundamentales de la materia:

* **Restauración de Imágenes:** Uso de modelos avanzados (SwinIR, GFPGAN) para eliminar ruido y reconstruir detalles.
* **Transformaciones de Intensidad:** El **Booster Final** (`ImageEnhance.Contrast`, `ImageEnhance.Color`) aplica una transformación al histograma para mejorar la saturación y el contraste general de la imagen.
* **Filtrado Espacial:** Uso de filtros de suavizado y operadores morfológicos de OpenCV para **generar máscaras de piel y ropa**.
* **Conversión de Espacio de Color:** Conversión a **B&W puro** (`.convert("L").convert("RGB")`) al inicio del flujo para optimizar la entrada del modelo de colorización.

---

## 6. 🔗 Instalación y Deployment

1.  **Instalar Dependencias:** Clonar el repositorio y ejecutar:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configurar API Key:** Configurar la clave `REPLICATE_API_TOKEN` en los **Secrets** de Hugging Face Spaces (o en `secrets.toml` localmente).
3.  **Ejecutar:**
    ```bash
    streamlit run app.py
    ```
4.  **Deployment Final (Obligatorio):** El sistema está diseñado para ser desplegado en **Hugging Face Spaces**.

---

## 7. 🚧 Limitaciones Conocidas

* **Latencia y Cuota de API:** El sistema depende del rendimiento de las APIs de Replicate. **El sistema fallará por `status: 402` o `429` si la cuenta no tiene saldo suficiente o se excede el límite de velocidad.**
* **Artefactos de Blending (GFPGAN):** Puede aparecer una sutil "costura" alrededor de los rostros reconstruidos si el fondo es muy contrastante.

## 8. 📝 Autor

**Raquel Mallqui Espinoza** *Estudiante de Tecnicatura Superior en Ciencias de Datos e IA - IFTS 24* *Año: 2025*

https://github.com/RaquelMallqui1/Tecnicas-de-Procesamiento-Digital-de-Imagenes.git