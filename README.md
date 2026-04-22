## DeepCheck AI: Plataforma Full-Stack de IA Privada y Monitorización Local

DeepCheck AI es un ecosistema integral diseñado para la ejecución de modelos de lenguaje (LLM) en infraestructuras privadas. Este proyecto nace como respuesta a la necesidad de implementar soluciones de Inteligencia Artificial que garanticen la soberanía de los datos, eliminando la dependencia de nubes externas y asegurando el cumplimiento normativo (RGPD).

## 🎯 ¿Qué problema resuelve?
En el contexto actual, el uso de IA suele implicar el envío de información sensible a servidores de terceros (OpenAI, Anthropic, etc.). **DeepCheck AI** soluciona este riesgo mediante la **IA On-Premise (Edge AI)**:
- **Privacidad absoluta:** Los datos se procesan íntegramente en el hardware local.
- **Soberanía tecnológica:** Control total sobre el motor de inferencia y los pesos del modelo.
- **Transparencia técnica:** Monitorización en tiempo real de cómo el software impacta en los recursos del hardware.

## 🛠️ Tecnologías Utilizadas
El proyecto ha sido construido utilizando un stack robusto enfocado en el rendimiento y la escalabilidad:
- **Backend:** FastAPI (Python 3.11) para una gestión asíncrona de alto rendimiento.
- **IA Engine:** Ollama ejecutando modelos como **DeepSeek** y **Qwen 2.5** de forma local.
- **Infraestructura:** Docker Compose para la orquestación de microservicios.
- **Base de Datos:** PostgreSQL 15 para persistencia relacional de chats y usuarios.
- **Telemetría:** `psutil` para la instrumentación y captura de métricas de hardware (CPU/RAM).
- **Seguridad:** Autenticación Stateless mediante **JWT (JSON Web Tokens)** y encriptación de credenciales (Bcrypt).
- **Networking:** Proxy inverso con Nginx para enrutamiento seguro.
  
## 🗂️ Estructura del Proyecto
El repositorio sigue las mejores prácticas de separación de responsabilidades:

```text
├── backend/                  # API Rest (FastAPI) y Modelos de Datos
│   ├── brain.py              # Controlador principal y Endpoints
│   ├── tablas.py             # Modelos ORM (SQLAlchemy)
│   ├── database.py           # Conector PostgreSQL
│   ├── init_db.sql           # Script de inicialización DDL
│   └── Dockerfile            # Construcción de la imagen Python
├── webui/                    # Frontend SPA (Vanilla JS + CSS)
│   ├── Acceso/               # Vistas de Login / Registro
│   ├── Admin/                # Dashboard de telemetría (psutil)
│   ├── Chat/                 # Interfaz principal de IA
│   └── assets/               # CSS monolítico y Router lógico
├── docker-compose.yml        # Orquestador de la infraestructura
├── nginx.conf                # Configuración de enrutamiento del Proxy Inverso
└── .env.example              # Plantilla de variables de entorno seguras
```

## 🚀 Instalación y Ejecución
Para desplegar este entorno de forma local, asegúrate de tener instalados Docker y Docker Compose.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/deepcheck-ai.git](https://github.com/tu-usuario/deepcheck-ai.git)
