<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow.svg" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-green.svg" />
  <img src="https://img.shields.io/badge/Gemini_AI-Flash_1.5-blue.svg" />
  <img src="https://img.shields.io/badge/Telegram-Bot_API-blue.svg" />
</div>

<br />

<div align="center">
  <h1>🛒 Siri Smart Shopping List Bot</h1>
  <p><b>Tu asistente personal de compras impulsado por IA.</b></p>
  <p>Olvídate de anotar. Simplemente dítaselo a tu iPhone y deja que Gemini organice tu hogar.</p>

  <br />

  <a href="https://render.com/deploy?repo=https://github.com/BorjaDelgadoDev/chatboot-telegram">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</div>

---

## 📽️ ¿Cómo funciona?

1. **Voz a Datos**: Dictas la compra a Siri ("Oye Siri, añade pan, leche y un kilo de patatas").
2. **IA Multitarea**: Gemini 1.5 Flash limpia el audio y separa los items por categorías.
3. **Smart List**: El bot actualiza un **único mensaje fijado** en Telegram.
4. **Control Total**: Tacha productos con un click. El bot se encarga de limpiar el chat de mensajes extra.

---

## 🛠️ Instalación "One-Click" (Recomendado)

¿Quieres tu bot funcionando **ya**? Solo necesitas 3 cosas de antemano:

1. **Telegram Token**: Pídeselo a [@BotFather](https://t.me/botfather). (**Importante**: Desactiva el *Privacy Mode* en los ajustes del bot en BotFather).
2. **Gemini Key**: Consíguela gratis en [Google AI Studio](https://aistudio.google.com/app/apikey).
3. **Chat ID**: El ID de tu grupo (puedes sacarlo enviando un mensaje a [@userinfobot](https://t.me/userinfobot)).

### Pasos:
1. Pulsa el botón de **"Deploy to Render"** de arriba. (Si has hecho Fork, recuerda actualizar la URL en el enlace del botón en `README.md`).
2. Rellena los campos que te pedirá Render (Tokens e IDs).
3. Una vez esté "Live", ya puedes configurar tu Atajo de Siri.

---

## 📱 Configuración de Siri (Atajo de iOS)

Es la pieza final del puzzle. Crea un Atajo en tu iPhone:

| Paso | Acción | Configuración |
| :--- | :--- | :--- |
| **1** | 🎤 **Dictar texto** | Idioma: Español |
| **2** | 🌐 **Obtener contenido de URL** | URL: `https://TU-URL-DE-RENDER.com/siri` |
| **3** | ⚙️ **Método** | `POST` |
| **4** | 🔑 **Encabezados** | `X-Auth-Token` : `Tu Token (SIRI_AUTH_TOKEN)` |
| **5** | 📦 **Cuerpo JSON** | Llave: `text`, Valor: `Texto dictado` |

---

## 🧩 FAQ - Preguntas Frecuentes

### Mi bot no borra los "Hola" del grupo... 🧹
Asegúrate de haber desactivado el **Privacy Mode** hablando con @BotFather (`Bot Settings > Group Privacy > Turn Off`). También debe ser **Administrador** con permiso de borrado.

### ¿Se pierde la lista si se apaga el servidor? 📌
¡No! Aunque usemos SQLite, el bot **fija la lista** en el chat. Al reiniciar, el bot busca el mensaje fijado y recupera toda la información automáticamente.

### ¿Puedo usarlo con mi pareja? 👫
¡Claro! Solo tenéis que estar los dos en el mismo grupo. Ambos podéis dictar a vuestros iPhones (configurando el mismo Atajo) y el bot actualizará la lista para ambos.

---

<div align="center">
  <sub>Hecho con ❤️ para un hogar más organizado.</sub>
</div>
