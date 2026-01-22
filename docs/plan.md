Plan Técnico: Arquitectura Zero-Cost

1. Stack Tecnológico

Lenguaje: Python 3.10+

Framework Web: FastAPI (Ligero para webhooks).

IA: google-generativeai (Gemini 1.5 Flash - Free Tier).

Bot Library: python-telegram-bot.

Base de Datos: SQLite3 (Local: compra.db).

Configuración: python-dotenv.

Hosting: Render (Plan gratis).

2. Esquema de Datos (SQLite)

Tabla items: id, name, category, quantity, created_at.

Tabla bot_state: key (PK), value. (Almacena master_message_id y chat_id).

3. Estructura de Archivos

.
├── main.py             # Punto de entrada y Endpoints (Siri/Webhook)
├── bot_logic.py        # Generación de mensajes y teclados
├── database.py         # Conexión y CRUD de SQLite
├── ai_handler.py       # Lógica de Gemini (Prompt Engineering)
├── .env                # Variables de entorno (EXCLUIDO DE GIT)
└── requirements.txt    # Dependencias de Python


4. Estrategia de Prueba (Ngrok)

Se utilizará Ngrok para exponer el puerto local (8000) a una URL pública. El Atajo de Siri apuntará a https://tu-id-ngrok.ngrok-free.app/siri para probar la integración real desde el móvil antes de subir a Render.