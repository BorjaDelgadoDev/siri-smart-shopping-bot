<div align="center">
  <img src="https://img.shields.io/badge/Versión-Fácil-orange.svg" />
  <img src="https://img.shields.io/badge/Idioma-Español-red.svg" />
  <img src="https://img.shields.io/badge/IA-Gemini-blue.svg" />
</div>

<br />

<div align="center">
  <h1>🛒 Tu Lista de la Compra Mágica</h1>
  <p><b>¡Oye Siri, añade pan y leche!</b></p>
  <p>Un sistema inteligente que organiza tu compra familiar en Telegram usando Inteligencia Artificial.</p>
</div>

---

## � ¿Qué hace este bot?
Este proyecto te permite dictarle a tu iPhone lo que te falta en la cocina. El sistema usa la IA de Google para categorizarlo todo (Lácteos, Frutas, Limpieza...) y lo pone en un único mensaje en un chat de Telegram compartido con tu pareja o familia. ¡Nada de mensajes sueltos!

---

## 🛠️ Guía "Para Humanos" (Paso a Paso)

No hace falta que sepas programar. Sigue estos pasos y lo tendrás en 10 minutos:

### 1. Prepara tu Chat en Telegram 💬
1. Busca a `@BotFather` en Telegram y dile `/newbot`. Ponle un nombre y guarda el **Token** que te dará (es un churro largo de letras y números).
2. Habla con `@BotFather` de nuevo, entra en `Bot Settings` -> `Group Privacy` y dale a **Turn Off** (esto es fundamental para que el bot pueda limpiar el chat).
3. Crea un grupo en Telegram con tu pareja/familia y añade tu nuevo bot.
4. **Haz al bot Administrador** del grupo.
5. Busca a `@userinfobot`, mándale un "Hola" y guarda tu **ID** (un número de 9 o 10 dígitos). El ID del grupo también te hará falta (empieza por `-`).

### 2. Saca tu "Cerebro" de IA 🧠
1. Entra en [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Pulsa en **"Create API Key"**. Guarda ese código. Es gratis y es lo que permite al bot entender lo que dices.

### 3. Ponlo en marcha en Internet 🚀
Usaremos **Render**, que es como un "parking" gratuito para el bot:
1. Hazte una cuenta en [Render.com](https://render.com).
2. Haz una copia de este proyecto pulsando el botón **"Fork"** arriba a la derecha en GitHub.
3. En Render, busca **"New +"** -> **"Web Service"**.
4. Conecta tu copia personal del proyecto.
5. En la sección **"Environment Variables"**, añade estos nombres y pega tus códigos:
   - `TELEGRAM_TOKEN`: (El que te dio BotFather).
   - `GEMINI_API_KEY`: (Tu clave de Google).
   - `CHAT_ID`: (El ID del grupo de Telegram).
   - `AUTHORIZED_USERS`: (Tu ID personal de números).
   - `SIRI_AUTH_TOKEN`: (Invéntate una palabra secreta, la que quieras).
   - `BASE_URL`: (La dirección que te asigne Render al final, termina en `.onrender.com`).
6. Pulsa en **"Deploy"** y espera a que ponga "Live" en verde.

### 4. Configura Siri en tu iPhone 📱
1. Abre la app **Atajos** de tu iPhone y crea uno nuevo llamado *"Añade a la compra"*.
2. Añade la acción **"Dictar texto"**.
3. Añade la acción **"Obtener contenido de URL"** y rellénala así:
   - **URL**: Pega tu dirección de Render terminada en `/siri`.
   - **Método**: Cámbialo a `POST`.
   - **Encabezados**: Añade uno con la clave `X-Auth-Token` y tu palabra secreta.
   - **Cuerpo JSON**: Añade un campo de texto llamado `text` y selecciona la variable "Texto dictado".
4. ¡Dile a tu iPhone: *"Oye Siri, añade a la compra"*!

---

## � ¿Por qué te va a encantar?
*   ✅ **Chat Impoluto**: El bot borra cualquier mensaje que no sea la lista. Solo verás un mensaje activo.
*   ✅ **Orden Total**: La IA organiza los productos por pasillos del super.
*   ✅ **Botones Reales**: Cuando estés en el super, solo pulsa el botón del producto y desaparecerá de la lista.
*   ✅ **Memoria Inmortal**: Aunque el servidor se apague, el bot recuerda la lista porque está "anclada" arriba en tu chat.

---

<div align="center">
  <sub>Diseñado para que la tecnología te ayude en el día a día. ❤️</sub>
</div>
