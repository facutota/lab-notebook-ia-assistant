# 🧠 Lab Notebook AI Assistant

## Arquitectura e Idea General del Proyecto

---

## 🎯 Objetivo del proyecto

Construir una aplicación web que funcione como un **cuaderno de laboratorio inteligente**, donde los usuarios puedan:

* Registrar experimentos
* Consultar historial
* Analizar resultados
* Interactuar con un **agente de IA** que los asista

El diferencial clave es la integración de **IA + datos estructurados + automatización**.

---

## 💡 Idea central

Este proyecto no es solo un CRUD de experimentos.

Es un sistema que combina:

* 📄 **Datos estructurados** (base de datos)
* 📚 **Conocimiento** (RAG / documentos)
* 🤖 **Agentes de IA** (Azure Foundry)

👉 Para crear un **asistente inteligente que entiende y actúa sobre los experimentos**.

---

## 🧩 Componentes principales

### 1. Frontend (apps/web)

* Next.js + Tailwind
* Interfaz tipo Notion / dashboard
* Permite:

  * ver experimentos
  * crear nuevos
  * ver detalles
  * interactuar con el asistente

---

### 2. Backend (apps/api)

* API REST (FastAPI o similar)
* Maneja:

  * lógica de negocio
  * acceso a base de datos
  * validaciones

Ejemplo de endpoints:

* `GET /experiments`
* `POST /experiments`
* `GET /experiments/{id}`
* `PATCH /experiments/{id}`

---

### 3. Base de datos

* PostgreSQL (Supabase / Render)
* Guarda:

  * experimentos
  * notas
  * resultados
  * estado

👉 Fuente de verdad del sistema

---

### 4. Agente de IA (agents/foundry)

Configurado en Azure Foundry.

Responsabilidades:

* entender preguntas del usuario
* decidir cuándo usar herramientas
* generar respuestas inteligentes

---

### 5. Tools (OpenAPI / funciones)

Permiten que el agente:

* consulte datos reales
* ejecute acciones

Ejemplo:

* obtener experimentos
* analizar resultados
* sugerir mejoras

---

## 🔄 Flujo general del sistema

```text
Usuario (Frontend)
↓
Next.js (UI)
↓
Backend API
↓
Base de datos
↑
Agente de IA (Azure Foundry)
↓
Tools (OpenAPI → API)
```

---

## 🧠 Cómo funciona el agente

El agente NO accede directo a la base de datos.

Funciona así:

1. El usuario hace una pregunta:

   > “Mostrame experimentos fallidos”

2. El agente decide:
   👉 “Necesito datos → llamo una tool”

3. Usa OpenAPI:
   → llama al backend

4. El backend responde con datos reales

5. El agente arma la respuesta final

---

## 🧪 Ejemplos de uso

### Caso 1: consulta

Usuario:

> “¿Qué experimentos fallaron esta semana?”

Flujo:

* agente → tool → backend → DB → respuesta

---

### Caso 2: análisis

Usuario:

> “Resumí este experimento”

Flujo:

* agente usa contexto + datos
* genera resumen

---

### Caso 3: recomendación

Usuario:

> “¿Cómo puedo mejorar este experimento?”

Flujo:

* analiza resultados
* sugiere mejoras

---

## 🧱 Arquitectura del repositorio

```bash
lab-notebook-ai-assistant/
  apps/
    web/        # frontend
    api/        # backend
  agents/
    foundry/    # agente + openapi
  packages/
    shared/     # tipos compartidos (opcional)
  docs/
    architecture.md
```

---

## 👥 Organización del equipo

### Frontend

* UI
* componentes
* navegación
* integración con API

### Backend

* endpoints
* modelos
* lógica

### AI / Agent

* agent.yaml
* tools
* pruebas en Foundry

### Integración

* deploy
* conexión entre sistemas
* testing

---

## 🚀 Stack tecnológico

* Frontend: Next.js + Tailwind
* Backend: FastAPI / Node
* DB: PostgreSQL
* AI: Azure Foundry (Agents)
* Integración: OpenAPI

---

## ⚠️ Decisiones importantes

### ✔️ Usamos OpenAPI

Para conectar el agente con el backend

### ✔️ No lógica en el frontend

Todo lo importante va en backend

### ✔️ El agente no inventa datos

Siempre usa tools si necesita datos

---

## 🎯 Qué queremos mostrar en el hackatón

* UI clara y usable
* Experimentos reales (mock o DB)
* Agente funcionando
* Integración completa:
  👉 usuario → IA → datos → respuesta

---

## 🧠 Frase clave del proyecto

> “Un copiloto inteligente para científicos que combina datos estructurados, conocimiento y agentes de IA para mejorar experimentos.”

---

## 📌 Estado inicial del proyecto

Primera fase:

* UI funcional
* mock data
* estructura completa

Segunda fase:

* backend real
* DB conectada
* agente integrado

Tercera fase:

* análisis inteligente
* mejoras UX
* demo final

---

## ✅ Resultado esperado

Un sistema donde:

* el usuario interactúa con una UI moderna
* puede gestionar experimentos
* y tiene un asistente de IA que:

  * entiende
  * consulta datos reales
  * y aporta valor

---

## 🔚 Resumen

Este proyecto combina:

* CRUD tradicional
* * IA (agentes)
* * integración real (tools)

👉 para construir algo mucho más potente que un simple sistema de registro.
