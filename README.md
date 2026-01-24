<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow.svg" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" />
  <img src="https://img.shields.io/badge/Gemini_AI-Flash_1.5-blue.svg" />
  <img src="https://img.shields.io/badge/Telegram-Bot_API-blue.svg" />
  <img src="https://img.shields.io/badge/License-MIT-gray.svg" />
</div>

<br />

<div align="center">
  <h1>🛒 Siri Smart Shopping List Bot</h1>
  <p><b>Transforma tu voz en una lista de la compra inteligente, categorizada y libre de spam.</b></p>
</div>

---

## 🌟 La Experiencia
Olvida los chats llenos de mensajes sueltos. Con este bot, la gestión de tu hogar sube de nivel:

1. **"Oye Siri, añade a la compra..."** 🗣️
2. La **IA (Gemini)** separa los productos y les asigna su pasillo/categoría automáticamente. 🧠
3. Un **único mensaje maestro** se actualiza en vuestro grupo de Telegram. 📌
4. Tachas los productos con un toque mediante **botones interactivos**. ✅

---

## 🛠️ Guía Maestra de Configuración (Paso a Paso)

Sigue estos pasos en orden para tener tu bot funcionando al 100%:

### 1️⃣ Preparación de Telegram
1. Habla con [@BotFather](https://t.me/botfather) y crea un nuevo bot con `/newbot`. Guarda el **Token**.
2. **Importante**: Manda `/mybots`, elige tu bot, ve a `Bot Settings` > `Group Privacy` y pulsa **Turn Off** (*Privacy mode is disabled*). Esto permite al bot limpiar el chat.
3. Crea un grupo en Telegram con tu pareja/familia y añade al bot.
4. Nombra al bot **Administrador** del grupo y asegúrate de que tenga permiso para **Eliminar mensajes** y **Fijar mensajes**.
5. Obtén el `CHAT_ID` del grupo (puedes usar @userinfobot o similares). Los IDs de grupo suelen empezar con `-100`.

### 2️⃣ Clave de Inteligencia Artificial
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Crea una **API Key** gratuita para Gemini. Esta es la que categorizará tus productos.

### 3️⃣ Despliegue del Servidor (Render)
1. Haz un Fork de este repositorio en tu cuenta de GitHub.
2. Crea una cuenta en [Render.com](https://render.com) y pulsa en **New > Web Service**.
3. Conecta tu repositorio de GitHub.
4. En **Environment Variables**, añade:
   - `TELEGRAM_TOKEN`: El token de BotFather.
   - `GEMINI_API_KEY`: Tu clave de Google.
   - `CHAT_ID`: El ID del grupo de Telegram.
   - `SIRI_AUTH_TOKEN`: Una contraseña inventada por ti (ej: `MiCasaSegura123`).
   - `AUTHORIZED_USERS`: Tu ID de Telegram (para que nadie más pueda usar tu bot).
5. Pulsa **Deploy**. Una vez esté "Live", copia la URL (ej: `https://mi-bot.onrender.com`).

### 4️⃣ Activación de Botones (Webhook)
Para que Telegram sepa dónde enviar los clics de los botones:
1. Abre una terminal en tu ordenador.
2. Ejecuta: `python3 set_webhook.py https://tu-url-de-render.com`
3. Si recibes `{"ok":true}`, los botones ya funcionan.

### 5️⃣ Configuración de Siri (Atajo de iOS)
1. Abre la app **Atajos** en tu iPhone y crea uno nuevo llamado *"Añade a la compra"*.
2. Añade la acción **"Dictar texto"**.
3. Añade la acción **"Obtener contenido de URL"**:
   - **URL**: `https://tu-url-de-render.com/siri`
   - **Método**: `POST`
   - **Encabezados**: Añade `X-Auth-Token` con tu `SIRI_AUTH_TOKEN`.
   - **Cuerpo JSON**: Añade la clave `text` con el valor `Texto dictado`.
4. ¡Pruébalo! Di: *"Oye Siri, añade a la compra manzanas y leche"*.

---

## ✨ Características Premium

- 🟢 **Master Message Concept**: Solo existe UN mensaje que se edita mágicamente.
- 📂 **Categorización Dinámica**: Frutos, Lácteos, Limpieza... todo en su sitio gracias a la IA.
- 🧹 **Modo Janitor (Conserje)**: El bot borra cualquier mensaje ajeno para mantener el chat impoluto.
- 📌 **Auto-Pin & Recovery**: El bot recupera la lista buscando el mensaje fijado automáticamente.
- 🔒 **Security First**: Autenticación por token y filtrado de usuarios.

---

<div align="center">
  <sub>Desarrollado con ❤️ para organizar hogares inteligentes.</sub>
</div>
