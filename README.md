# DeepCheck AI: Plataforma Full-Stack de IA Soberana y Monitorización Local

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
- **Base de Datos:** PostgreSQL 16 para persistencia relacional de chats y usuarios.
- **Telemetría:** `psutil` para la instrumentación y captura de métricas de hardware (CPU/RAM).
- **Seguridad:** Autenticación Stateless mediante **JWT (JSON Web Tokens)** y encriptación de credenciales.
- **Networking:** Proxy inverso con Nginx para enrutamiento seguro.

## 🏗️ Arquitectura del Sistema
El sistema opera mediante contenedores aislados que se comunican a través de una red virtual interna (`ai_net`). Esta arquitectura garantiza un despliegue repetible y seguro:
- **WebUI:** Interfaz Vanilla JS reactiva con transiciones de estado dinámicas.
- **API Brain:** Núcleo lógico que procesa la inferencia y gestiona la persistencia.
- **Admin Dashboard:** Panel de control para la monitorización de la salud del servidor.

## 🚀 Instalación y Ejecución
Para desplegar este entorno de forma local, asegúrate de tener instalados Docker y Docker Compose.

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/deepcheck-ai.git](https://github.com/tu-usuario/deepcheck-ai.git)
