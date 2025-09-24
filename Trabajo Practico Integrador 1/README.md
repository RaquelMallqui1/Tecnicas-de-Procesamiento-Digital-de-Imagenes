# 🌟 Trabajo Integrador 1: Sistema Básico de Análisis Automático de Documentos

## Introducción

Este repositorio presenta el **Trabajo Integrador 1** de la asignatura **"Técnicas de Procesamiento Digital de Imágenes"**. El objetivo principal es desarrollar un sistema básico capaz de pre-procesar y preparar documentos digitalizados para su posterior análisis o **Reconocimiento Óptico de Caracteres (OCR)**, abordando desafíos comunes en la digitalización.

El sistema está diseñado para aplicar técnicas de PDI estudiadas en el curso, tales como la **normalización de iluminación**, la **detección y corrección de rotación (deskewing)**, y la **mejora de la calidad visual**. El código fuente y la demostración se encuentran en el *notebook* adjunto.

---

## Contenido

Esta carpeta contiene todos los archivos necesarios para la ejecución y demostración del sistema de análisis de documentos:

| Archivo | Tipo | Descripción |
| :--- | :--- | :--- |
| **`Trabajo_Integrador_1.ipynb`** | Jupyter/Colab Notebook | **Código principal** del sistema. Contiene la implementación paso a paso de las técnicas de pre-procesamiento, el análisis y los resultados para cada una de las tres imágenes de prueba. |
| `documento_buena_calidad.jpg` | Datos de Entrada | Documento utilizado como **referencia (baseline)**, de buena calidad y sin problemas graves. |
| `documento_rotado.jpg` | Datos de Entrada | Documento que requiere la aplicación de técnicas de **detección y corrección de ángulo (deskew)**. |
| `documento_mala_luz.jpg` | Datos de Entrada | Documento con problemas de **iluminación no uniforme** (sombras), utilizado para demostrar técnicas de normalización. |

---

## Resumen del Sistema y Técnicas Aplicadas

El *notebook* implementa un flujo de trabajo de pre-procesamiento que aborda los desafíos presentados por los documentos de entrada.

### 🛠️ Flujo de Procesamiento

El sistema aplica una secuencia de pasos optimizada:

1.  **Carga y Conversión:** Carga de la imagen y conversión a escala de grises.
2.  **Normalización de Iluminación:** Aplicación de filtros o técnicas para corregir problemas de **iluminación** y **contraste** (ej. Ecualización de Histograma Adaptativa, Filtros de Homomorfismo o *Shadow Removal*).
3.  **Corrección de Rotación (Deskewing):** Uso de transformadas (ej. Transformada de Hough o análisis de momentos) para **detectar el ángulo de inclinación** del documento y rotarlo a la orientación correcta.
4.  **Binarización:** Aplicación de *thresholding* adaptativo (ej. `cv2.ADAPTIVE_THRESH_GAUSSIAN_C`) para convertir el documento a blanco y negro, separando el texto del fondo.

### Librerías Utilizadas

* **OpenCV (`cv2`):** Herramienta principal para todas las operaciones de procesamiento de imágenes.
* **Matplotlib (`plt`):** Utilizada para la visualización y comparación de los resultados (documento original vs. documento procesado).
* **NumPy (`np`):** Para la manipulación de los *arrays* de píxeles.

---

## 💻 ¿Cómo utilizar el Notebook de Colab?

El archivo **`Trabajo_Integrador_1.ipynb`** debe ejecutarse en **Google Colaboratory** para un entorno sin configuración.

1.  **Estructura:** Asegúrate de que las tres imágenes de documentos (`documento_buena_calidad.jpg`, `documento_rotado.jpg`, `documento_mala_luz.jpg`) estén accesibles para el *notebook* (idealmente, cargadas en la misma carpeta o montadas desde Google Drive).
2.  **Ejecución:** Abre el *notebook* directamente en Colab (usando el botón "Open in Colab" si estás en GitHub).
3.  **Secuencia:** Ejecuta todas las celdas de forma secuencial. El *notebook* está documentado para mostrar los resultados intermedios de cada técnica aplicada.

---

## 📧 Contacto y Licencia

### Contacto

Para consultas sobre la implementación del sistema o las técnicas de PDI utilizadas:

* **Nombre:** Raquel Mallqui 
* **Email:** 93854950@ifts24.edu.ar

### Licencia

Este proyecto está disponible para su **Uso Educativo y de Demostración** en el contexto de la materia. Se prohíbe su uso comercial sin consentimiento explícito.
