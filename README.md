# Reconocimiento de Diagramas de Flujo Dibujados a Mano

Un sistema inteligente que utiliza visión por computadora y OCR para reconocer y procesar diagramas de flujo dibujados a mano, convirtiendo imágenes en datos estructurados.

<img width="2308" height="1024" alt="diagram_flowchart_recognotion" src="https://github.com/user-attachments/assets/6bed90b9-e0c2-4659-89ac-ce6f967a27e2" />


## 🚀 Características

- **Detección de formas**: Reconoce automáticamente círculos, cuadrados, triángulos y flechas
- **OCR integrado**: Extrae texto de las formas usando Tesseract
- **Análisis de conexiones**: Detecta automáticamente las flechas y conexiones entre nodos
- **Múltiples interfaces**: Línea de comandos, GUI y servicio web Flask
- **Múltiples formatos de salida**: Genera archivos JSON, imágenes procesadas y texto estructurado
- **Procesamiento robusto**: Utiliza técnicas avanzadas de procesamiento de imágenes

## 📋 Requisitos

### Dependencias de Python
```
opencv-python==4.11.0.86
pytesseract==0.3.13
imutils==0.5.4
numpy==2.3.0
Pillow==11.2.1
tabulate==0.9.0
```

### Dependencias del sistema
- **Tesseract OCR**: Necesario para el reconocimiento de texto
  - Windows: Descargar desde [GitHub Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt install tesseract-ocr tesseract-ocr-spa`
  - macOS: `brew install tesseract`

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd hand_drawn_flowchart_recognition
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv env
# Windows
env\Scripts\activate
# Linux/macOS
source env/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📖 Uso

### 🖥️ Línea de comandos

**Uso básico:**
```bash
python flowchart_recognition.py -f imagen_diagrama.png
```

**Con parámetros personalizados:**
```bash
python flowchart_recognition.py -f imagen.png -p 30 -o 15 -a 35
```

**Uso interactivo:**
```bash
python flowchart_recognition.py
```

### 🖼️ Interfaz gráfica

```bash
python GUI.py
```

### 🌐 Servicio web Flask

```bash
python main.py
```

### ⚙️ Parámetros disponibles

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `-f, --filename` | Archivo de imagen a procesar (requerido) | - |
| `-p, --padding` | Distancia entre texto interno y contorno de formas | 25 |
| `-o, --offset` | Para decidir dirección de líneas curvas | 10 |
| `-a, --arrow` | Longitud de flecha para detección | 30 |

## 📊 Ejemplo de resultado

| Id | Name | Position | Shape | Line |
| - | - | - | - | - |
| 0 | DATABASE| Inside | square |  |
| 2 | LORD BALANCER | Inside | square | DATABASE |
| 4 | LMN | Inside | square | LORD BALANCER|

**Campos de resultado:**
- **Position**: `inside` (texto dentro de la forma) / `outside` (texto fuera)
- **Shape**: `triangle` / `square` / `circle` / `arrow`
- **Line**: nodos conectados hacia donde va

<img width="161" height="1072" alt="image" src="https://github.com/user-attachments/assets/4677325a-9752-4319-bf33-c52e783fd63f" />


## 📁 Estructura del proyecto

```
hand_drawn_flowchart_recognition/
├── flowchart_recognition.py    # Módulo principal de reconocimiento
├── convert_to_txt.py          # Procesador de resultados a texto
├── digital_diagram.py         # Utilidades para diagramas digitales
├── GUI.py                     # Interfaz gráfica de usuario
├── main.py                    # Servicio web Flask
├── app.py                     # Aplicación alternativa
├── verificacion.py            # Herramientas de verificación
├── requirements.txt           # Dependencias del proyecto
├── data.json                  # Resultados del reconocimiento (generado)
├── resultado_diagrama.txt     # Texto procesado (generado)
└── README.md                  # Este archivo
```

## 🔄 Flujo de trabajo

1. **Carga de imagen**: El sistema lee la imagen del diagrama de flujo
2. **Preprocesamiento**: Aplica filtros, umbralización y detección de bordes
3. **Detección de contornos**: Encuentra las formas geométricas
4. **Clasificación de formas**: Identifica círculos, cuadrados, triángulos y flechas
5. **Extracción de texto**: Usa OCR para leer el texto dentro de las formas
6. **Análisis de conexiones**: Detecta las flechas y sus conexiones
7. **Generación de salida**: Crea archivos JSON, imágenes y texto estructurado

## 📤 Archivos de salida

### 1. `data.json`
Contiene la estructura completa del diagrama:
```json
{
  "Node": [
    {
      "Id": 0,
      "Name": "INICIO",
      "Position": "Inside",
      "Shape": "circle",
      "Line": "PROCESO 1"
    }
  ]
}
```

### 2. Imagen procesada
- Archivo: `[nombre_original]_out_[timestamp].[extension]`
- Contiene: Contornos detectados, etiquetas y texto reconocido

### 3. `thresh.png`
Imagen umbralizada para análisis interno
<img width="792" height="1408" alt="thresh" src="https://github.com/user-attachments/assets/58f887a6-50cc-4511-a56e-e9f1f0fd896f" />


### 4. `resultado_diagrama.txt` (usando convert_to_txt.py)
Texto estructurado con comandos procesados

```json
INICIO
ADELANTE 6
IZQUIERDA 2
ADELANTE 3
DERECHA 3
ADELANTE
IZQUIERDA 2
ADELANTE 2
FIN
```

## 🔧 Módulo de conversión de texto

### convert_to_txt.py
Procesa el archivo JSON y convierte los textos reconocidos según reglas específicas:

```bash
python convert_to_txt.py
```

**Reglas de conversión:**
- `INI` → `INICIO`
- `ADELA` → `ADELANTE`
- `DERE` → `DERECHA`
- `QUI` → `IZQUIERDA`
- `FIN` → `FIN`

## 🎯 Consejos para mejores resultados

1. **Calidad de imagen**: Usa imágenes con buena resolución y contraste
2. **Formas claras**: Dibuja formas bien definidas y cerradas
3. **Texto legible**: Escribe con letra clara y tamaño adecuado
4. **Fondo limpio**: Evita fondos con ruido o texturas
5. **Líneas continuas**: Las flechas deben ser líneas continuas y claras

## 🔍 Troubleshooting

### Error: "TesseractNotFoundError"
```bash
# Verificar instalación
tesseract --version

# En Windows, agregar al PATH o configurar pytesseract
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Reconocimiento de texto deficiente
- Aumentar el parámetro `padding` para mejor extracción
- Verificar que el idioma esté configurado correctamente (`lang='spa'`)
- Mejorar la calidad de la imagen de entrada

### Formas no detectadas
- Ajustar los parámetros de umbralización
- Verificar que las formas estén cerradas
- Probar con diferentes valores de `offset` y `arrow`

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [OpenCV](https://opencv.org/) - Biblioteca de visión por computadora
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Motor de reconocimiento óptico de caracteres
- [imutils](https://github.com/jrosebr1/imutils) - Utilidades para procesamiento de imágenes

---

📧 Para preguntas o soporte, crear un issue en el repositorio.
