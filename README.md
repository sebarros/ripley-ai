# Ripley AI - Plataforma Inteligente de Atención al Cliente

Aplicación web desarrollada para Ripley Chile que integra un **Chatbot RAG**, un **Agente Inteligente con herramientas**, y un **Centro de Monitoreo**, permitiendo responder consultas, recomendar productos y visualizar métricas de uso en tiempo real.

---

# Descripción General

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

# Arquitectura del Sistema

<img width="1149" height="1369" alt="8f4d3a0e-966e-4e85-8545-72af5c1e3dc6" src="https://github.com/user-attachments/assets/1c97ad02-5709-494e-8138-c5da4594d3db" />

## Frontend

### `app.py`

Punto de entrada de la aplicación.

Permite navegar entre:

* Chatbot
* Agente
* Monitoreo

### `chatbot_page.py`

Interfaz conversacional del Chatbot RAG.

### `agent_page.py`

Interfaz conversacional del Agente Inteligente.

### `dashboard_page.py`

Panel de monitoreo y visualización de métricas.

---

## Backend

### `router.py`

Encargado de dirigir cada solicitud hacia:

* Chatbot
* Agente

También aplica:

* Validaciones
* Sanitización
* Rate limiting

---

## Chatbot RAG

### `chatbot.py`

Implementa:

* Embeddings OpenAI
* Base vectorial FAISS
* Recuperación de contexto
* Memoria conversacional
* Streaming de respuestas

---

## Agente Inteligente

### `ripley_agent.py`

Orquesta todo el flujo del agente:

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

## 3. Construir la imagen Docker

```bash
docker build -t ripley-ai .
```

---

## 4. Ejecutar el contenedor

```bash
docker run --rm -p 8501:8501 --env-file .env ripley-ai
```

---

## 5. Abrir la aplicación

Ingresa desde tu navegador a:

```text
http://localhost:8501
```

---

## 6. Verificación rápida

Ver contenedores:

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
