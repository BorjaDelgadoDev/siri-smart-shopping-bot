Tasks: Roadmap de Implementación

Fase 1: Setup y Cerebro (IA)

[x] [Setup] Crear entorno virtual y archivo .env.

[x] [DB] Crear database.py con funciones init_db, add_item y get_all_items.

[x] [IA] Crear ai_handler.py con el System Prompt para forzar salida JSON.

[x] [Test] Validar que la IA limpia frases complejas y devuelve una lista de objetos.

Fase 2: Endpoint de Siri y Pruebas Locales

[x] [API] Crear ruta POST /siri en main.py con validación de token.

[x] [Test] Usar Postman para enviar textos al endpoint y verificar que se guardan en la DB.

[x] [iOS] Configurar el Atajo de Siri para enviar voz a la URL local (vía Ngrok).

Fase 3: Telegram y Mensaje Maestro

[x] [Bot] Implementar render_list() en bot_logic.py para formatear el mensaje con emojis.

[x] [Bot] Lógica de persistencia de mensaje: Guardar y leer master_message_id.

[x] [Bot] Implementar el botón "Comprar" que elimina el item y refresca el mensaje.

Fase 4: Despliegue Final

[ ] [Deploy] Subir a GitHub (asegurando .gitignore para la DB y .env).

[ ] [Deploy] Configurar Webhook oficial de Telegram en Render.