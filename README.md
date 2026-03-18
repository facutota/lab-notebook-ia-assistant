<!-- HEADER -->

# 🤖 ALMA: AI Lab Multipurpose Assistant

Sistema de gestión de experimentos científicos con asistencia de IA para acelerar el ciclo de experimentación manteniendo rigor y seguridad.

<p align="center"> <img src="assets/logo-alma.png" alt="Logo ALMA" width="400"/> </p>

ALMA es un Agente de IA diseñado como un Cuaderno de Laboratorio Digital (ELN) inteligente que actúa como un grafo de conocimiento persistente para la gestión de experimentos científicos. El sistema permite documentar protocolos, registrar observaciones, almacenar resultados y consultar mediante IA todo el conocimiento generado.

[Demo: ]()

---

🎯 Módulos y Funcionalidades (MVP)


| Modulo                     | Descripcion                                                                                                                                                                             |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gestión de Experimentos         | CRUD de proyectos y experimentos con estructura jerárquica                                                           |
| Diario de Laboratorio        | Registro de anotaciones, observaciones y resultados |
| Almacenamiento de Archivos | Subida y gestión de PDFs, imágenes, CSVs en Blob Storage                                                                                |
| Procesamiento de Documentos     | OCR para imágenes y extracción de texto de PDFs                                                                                                                     |
| Asistente IA                      | Chat contextual con capacidad de grounding en documentos del laboratorio                                                                                               |
| Búsqueda Semántica                           | RAG sobre la base de conocimiento experimenta                                                                          |

🧠 Arquitectura del Sistema


| **Capa**                   | **Tecnologia**                   | **Descripción** |
| -------------------------- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
| Frotend     | React + Bootstrap | SPA con panel lateral de chat y visor de documentos|
| Backend API | Azure Function (Python) | Orquestador API y lógica de negocio |
| Base de datos            | Azure SQL (capa gratuita)           | Persistencia relacional de experiementos|
| Almacenamiento              | Azure Blob Storage  | Repositorio de documentos, imagenes y resultados|
| Busqueda vectorial | Azure AI Search | RAG sobre documentos cientificos |
| LLM | GPT-4o-mini | Razonamiento sobre protocolo y resultados |
| Procesamiento | Azure AI Vision | OCR y extracciion de tablas |

---

🛠️ Tecnologías usadas

| **Categoria**                     | **Tecnologia** |
| -------------------------- | -------------------------------- | 
| Cloud         | Azure (Resource Group, Storage Account, SQL Server)                                                          |
| Backend        | Azure Functions (Python) |
| IA/ML | Azure AI Agent Service, Azure AI Search, Azure AI Vision, GPT-4o-mini  |
| Frontend     | React, Bootstrap (por definir)|
| DevOps  | Git, Documentación técnica                                                                                              |

---

📦 Recursos Azure Desplegados

|**Recurso** |	Nombre |	Región |	Propósito |
| -------------------------- | -------------------------------- | -------------------------------- | -------------------------------- | 
|Resource Group |	rg-alma |	East US |	Contenedor principal|
Storage Account |	stalma01 |	East US |	Blob storage para archivos|
SQL Server |	svr-alma-01 |	West US |	Servidor de base de datos |
SQL Database |	db-free-sql-alma |	West US |	Base de datos transaccional |

---

🏗️ Funcionamiento de la Aplicación

🧩 Estrategia de Testeo

⭐ Capturas de Pantalla

🎥 Video Final del Proyecto

📄 Guía de Ejecución del Proyecto

⚙️ Instalación y Configuración

