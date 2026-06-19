<<<<<<< HEAD
# Ripley AI - Plataforma Inteligente de Atención al Cliente
=======
# Ripley Agent - Asistente Inteligente de Compras y Clima
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

Aplicación web desarrollada para Ripley Chile que integra un **Chatbot RAG**, un **Agente Inteligente con herramientas**, y un **Centro de Monitoreo**, permitiendo responder consultas, recomendar productos y visualizar métricas de uso en tiempo real.

---

<<<<<<< HEAD
# Descripción General
=======
## Descripción General
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

La plataforma está compuesta por tres módulos principales:

### 💬 Chatbot RAG

Asistente conversacional basado en GPT-4.1-mini que responde utilizando una base de conocimiento de Ripley Chile.

Características:

* Recuperación de contexto mediante FAISS.
* Memoria conversacional.
* Respuestas contextualizadas.
* Protección contra Prompt Injection.
* Streaming de respuestas en tiempo real.

### 🤖 Agente Inteligente

Agente autónomo capaz de utilizar herramientas externas para resolver tareas específicas.

Características:

* Detección de intención mediante Planner.
* Consulta de clima.
* Búsqueda de productos.
* Catálogo híbrido (FakeStore API + catálogo local).
* Memoria corta y larga.
* Recomendaciones contextuales.

### 📊 Centro de Monitoreo

Dashboard desarrollado en Streamlit para visualizar el comportamiento del sistema.

Incluye:

* Total de consultas.
* Latencia promedio.
* Tasa de errores.
* Historial completo de interacciones.
* Monitoreo de Chatbot y Agente en un único panel.

---

<<<<<<< HEAD
# Arquitectura del Sistema
=======
## Arquitectura del Sistema
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

## Frontend

### `app.py`

<<<<<<< HEAD
Punto de entrada de la aplicación.
=======
### 2. `planner.py` (Clasificador de intención)
- Detecta la intención del usuario usando regex o reglas simples
- Decide qué herramienta usar:
  - clima
  - búsqueda de productos
  - listado de productos
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

Permite navegar entre:

* Chatbot
* Agente
* Monitoreo

<<<<<<< HEAD
### `chatbot_page.py`
=======
- `weather_tool`: consulta clima por ciudad
- `search_product_tool`: busca productos por texto
- `list_products_tool`: muestra catálogo
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

Interfaz conversacional del Chatbot RAG.

<<<<<<< HEAD
### `agent_page.py`

Interfaz conversacional del Agente Inteligente.

### `dashboard_page.py`

Panel de monitoreo y visualización de métricas.

---

## Backend
=======
### 5. `memory.py` (Sistema de memoria)
- Memoria corta (últimos 15 mensajes)
- Memoria larga (perfil del usuario)
- Estado conversacional (ej: recomendación post-clima)
- Recuperación básica por similitud de texto

---

## Flujo del Agente
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

### `router.py`

Encargado de dirigir cada solicitud hacia:

* Chatbot
* Agente

También aplica:

* Validaciones
* Sanitización
* Rate limiting

---

<<<<<<< HEAD
## Chatbot RAG
=======
## Funcionalidad de Clima + Recomendación
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

### `chatbot.py`

Implementa:

* Embeddings OpenAI
* Base vectorial FAISS
* Recuperación de contexto
* Memoria conversacional
* Streaming de respuestas

---

<<<<<<< HEAD
## Agente Inteligente
=======
## Funcionalidades de Productos
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

### `ripley_agent.py`

Orquesta todo el flujo del agente:

<<<<<<< HEAD
* Planner
* Herramientas
* Memoria
* LLM
* Observabilidad

### `planner.py`

Clasifica la intención del usuario y selecciona la herramienta adecuada.

Intenciones soportadas:

* Clima
* Búsqueda de productos
* Catálogo

### `tools.py`

Herramientas disponibles:

* `weather_tool`
* `search_product_tool`
* `list_products_tool`

### `memory.py`

Sistema de memoria del agente:

* Memoria corta
* Perfil de usuario
* Recuperación semántica

---

## Integraciones Externas

### OpenAI / Azure OpenAI

Utilizado para:

* Chatbot RAG
* Agente Inteligente
* Embeddings

### Open-Meteo

Consulta meteorológica por ciudad.

### FakeStore API

Fuente adicional de productos.

### Catálogo Local

Archivo JSON propio con productos en CLP.

---

# Flujo General del Sistema

1. Usuario envía una consulta.
2. El Router valida y procesa la solicitud.
3. La consulta es enviada al Chatbot o al Agente.
4. Se recupera contexto o se ejecutan herramientas.
5. GPT genera la respuesta.
6. La interacción se registra en el sistema de monitoreo.
7. Los resultados aparecen en tiempo real en el Dashboard.

---

# 📊 Observabilidad

Todas las interacciones son almacenadas en:

```text
data/logs/logs.csv
```

Cada registro contiene:

* Timestamp
* Tipo (chatbot o agent)
* Pregunta
* Respuesta
* Intención
* Latencia
* Error

---

# Cómo ejecutar el proyecto

=======
Fuente de datos: https://fakestoreapi.com

---

# Cómo ejecutar el proyecto

>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956
## 1. Requisitos previos

Antes de ejecutar, asegúrate de tener:

* Docker instalado
* API Key válida
* Archivo `.env`

---

## 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
GITHUB_TOKEN=tu_api_key
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

Importante:

* No usar comillas.
* No dejar espacios extra.
* No subir el archivo `.env` al repositorio.

---

<<<<<<< HEAD
## 3. Construir la imagen Docker
=======
## 3. Ejecutar el contenedor
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

```bash
docker build -t ripley-ai .
```

---

## 4. Ejecutar el contenedor

```bash
docker run --rm -p 8501:8501 --env-file .env ripley-ai
```
<<<<<<< HEAD
=======
## 4. Abrir la aplicación
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

---

## 5. Abrir la aplicación

Ingresa desde tu navegador a:

```text
http://localhost:8501
```

<<<<<<< HEAD
---

## 6. Verificación rápida

Ver contenedores:
=======
## 5. Verificación rápida (si algo falla)
>>>>>>> febced3cfab885ed3fe6efeb6fff4f574c1eb956

```bash
docker ps -a
```

Ver logs:

```bash
docker logs <container_id>
```

---

# Tecnologías Utilizadas

* Python 3.11
* Streamlit
* LangChain
* OpenAI
* FAISS
* Pandas
* Plotly
* Docker
* Open-Meteo API
* FakeStore API