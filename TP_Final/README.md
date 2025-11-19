# Restauración y Colorización de Fotos Antiguas

Aplicación web para restaurar y colorizar fotos antiguas utilizando modelos de difusión avanzados y análisis visual con IA.

## Características

- **Restauración Facial**: Utiliza GFPGAN vía Replicate para restaurar rostros dañados
- **Colorización**: Emplea DeOldify vía Replicate para colorizar imágenes en blanco y negro
- **Preprocesamiento**: Corrección automática de iluminación, reducción de ruido y mejora de contraste
- **Análisis Visual**: Comparación semántica con CLIP y clasificación con ViT
- **Métricas de Calidad**: SSIM, PSNR y evaluación automática de mejora
- **Interfaz Interactiva**: Streamlit con controles avanzados y vista comparativa

## Instalación

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu API key de Replicate en las variables de entorno:
   ```bash
   export REPLICATE_API_TOKEN=tu_token_aqui
   ```
4. Ejecuta la aplicación:
   ```bash
   streamlit run app.py
   ```

## Estructura del Proyecto

```
TP_Final/
├── app.py                 # Interfaz principal de Streamlit
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
├── config/
│   └── config.yaml       # Configuraciones y API keys
├── models/
│   ├── diffusion.py      # Modelos de restauración y colorización
│   └── analysis.py       # Análisis con CLIP y ViT
└── utils/
    ├── image_utils.py    # Utilidades de procesamiento de imágenes
    └── ui_utils.py       # Utilidades de interfaz
```

## Uso

1. Sube una imagen antigua (JPG, PNG)
2. Ajusta el tono de piel y color de ropa en la barra lateral
3. Haz clic en "Procesar imagen"
4. Visualiza los resultados con metadatos y análisis

## Tecnologías Utilizadas

- **Streamlit**: Interfaz web
- **PIL/Pillow**: Procesamiento básico de imágenes
- **OpenCV**: Operaciones avanzadas de visión por computadora
- **Replicate**: API para modelos de IA (DeOldify, GFPGAN)
- **Transformers (Hugging Face)**: CLIP y ViT para análisis
- **Scikit-Image**: Métricas de calidad de imagen

## Configuración

Edita `config/config.yaml` para ajustar parámetros:

- URLs de modelos en Replicate
- Parámetros por defecto del procesamiento
- Configuraciones de análisis

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.