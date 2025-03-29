# ✨ NicoBot - Telegram Bot

Bienvenido a *NicoBot*, un bot multifunción para Telegram que te permite:

- Consultar el clima actual ☀️  
- Analizar el sentimiento de un texto 📊  
- Buscar vuelos (arribos y salidas) desde aeropuertos ✈️  
- Contar cuántas veces interactuaste con el bot 🔢  

> Desarrollado con Python, Redis y desplegado usando Docker. Integra APIs de OpenWeather, FlightAware y OpenAI.

> 🌐 Actualmente hosteado en Google Cloud Platform (GCP), accesible desde cualquier lugar.

---

## 🧠 ¿Por qué incluir vuelos?

La funcionalidad de vuelos se eligió para ampliar el valor del bot en contextos reales como viajes, vuelos demorados o llegada de familiares. Muchos usuarios buscan datos sobre vuelos sin necesidad de entrar a sitios específicos: *NicoBot* resume esta información con solo escribir un comando o presionar un botón.

---

## 🚀 Comandos disponibles

- `/start`: Inicia la conversación y muestra el menú principal.  
- `/help`: Muestra ayuda sobre cómo usar el bot.  
- `/clima [ciudad]`: Consulta el clima actual en cualquier ciudad del mundo.  
- `/vuelos`: Activa el menú para buscar vuelos por aeropuerto.  
- `/analisis [texto]`: Analiza el sentimiento de un texto (positivo, negativo, neutral).  
- `/contador`: Muestra cuántas veces interactuaste con el bot.  

---

## 🤖 Funcionalidades destacadas

### ☁️ Clima

- Usa OpenWeatherMap para consultar el estado actual.  
- Integra OpenAI para darte un consejo útil y contextual en base al clima (ej. "No olvides el paraguas").  
- Uso: `/clima Montevideo` o usando el botón “Quiero ver el clima”.

### ✈️ Vuelos

- Conectado a la API de FlightAware.  
- Permite buscar *arribos* o *salidas* desde un aeropuerto usando el código IATA (ej. `MVD` para Montevideo).  
- Muestra:
  - Nombre del vuelo y aerolínea.  
  - Origen o destino.  
  - Hora estimada.  
  - Estado (a tiempo, cancelado, etc.).  
- Usa botones para elegir el tipo de búsqueda.  
- Uso típico: `/vuelos` → Elegís “Arribos” → Enviás `MVD`.

### 📊 Análisis de Sentimiento

- Analiza cualquier texto usando OpenAI.  
- Clasifica el mensaje como positivo, negativo o neutral.  
- Ejemplo: `/analisis Hoy me siento genial` → “😊 Positivo: se percibe entusiasmo y bienestar.”

### 🔢 Contador de interacciones

- Usa Redis para contar cuántas veces interactuaste con el bot.  
- Guarda el estado por usuario y responde con mensajes dinámicos.  
- Ejemplo: “💪 5 interacciones... ¡Te estás volviendo un experto! 😎”

---

## 🧪 Requisitos

- Python 3.12+  
- Redis (para contar interacciones)  
- Claves API:
  - `TELEGRAM_TOKEN`  
  - `OPENWEATHER_API_KEY`  
  - `OPENAI_API_KEY`  
  - `FLIGHTAWARE_API_KEY`  

---

## 🐳 Cómo ejecutar (Docker)

1. Clonar el repositorio y crear el archivo `.env` con las variables anteriores.
2. Ejecutar:

```bash
docker-compose up --build
