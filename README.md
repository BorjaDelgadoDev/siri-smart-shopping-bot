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
  <p>Convierte tus notas de voz en una lista organizada automáticamente por la IA de Google Gemini.</p>
</div>

---

## 📽️ ¿Cómo funciona el Sistema?

1. **Voz a Datos**: Dictas la compra a Siri ("Oye Siri, añade pan, leche y un kilo de patatas").
2. **IA Multitarea**: Gemini 1.5 Flash procesa el texto y separa los productos por categorías lógicas.
3. **Smart List**: El bot actualiza un **único mensaje maestro fijado** en vuestro grupo de Telegram.
4. **Interactividad**: Tacha productos con un click. El bot mantiene el chat limpio de spam (Janitor Mode).

---

## � Guía de Despliegue Express

Para que tu bot cobre vida en 5 minutos, sigue este flujo universal (válido para cualquier fork):

### 1️⃣ Setup de Telegram & IA
*   **Telegram**: Crea tu bot en [@BotFather](https://t.me/botfather). Desactiva el *Privacy Mode* en los ajustes del bot para que pueda limpiar el chat.
*   **Google AI**: Consigue tu API Key gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2️⃣ Despliegue en la Nube (Render / Railway / etc.)
No necesitas comandos complicados. Simplemente conecta tu copia (Fork) del repositorio a tu plataforma favorita:

*   **Paso A**: Crea un nuevo **Web Service**.
*   **Paso B**: Conecta este repositorio de GitHub.
*   **Paso C**: Configura las **Variables de Entorno**:
    - `TELEGRAM_TOKEN`, `GEMINI_API_KEY`, `CHAT_ID`.
    - `SIRI_AUTH_TOKEN`: Una clave frase secreta inventada por ti.
    - `BASE_URL`: La URL que te asigne la plataforma (ej: `https://mi-compra.onrender.com`). **¡Esto activa los botones e IA automáticamente!**

---

## 📱 Conexión con Siri (iOS Shortcuts)

Configura este sencillo flujo en la App **Atajos** de tu iPhone para dictar la compra:

| Acción | Detalle de Configuración |
| :--- | :--- |
| 🎤 **Dictar texto** | Idioma: Español |
| 🌐 **Contenido de URL** | URL: `https://TU-URL-PUBLICA.com/siri` |
| ⚙️ **Método** | `POST` |
| 🔑 **Encabezados** | `X-Auth-Token` : `Tu Token (SIRI_AUTH_TOKEN)` |
| 📦 **Cuerpo JSON** | Llave: `text` -> Valor: `Texto dictado` |

---

## 💡 ¿Por qué es especial este Bot?

- **Un solo mensaje**: Se acabó el scroll. La lista es un ente vivo que se edita a sí mismo.
- **Janitor Mode**: El bot monitoriza el grupo y borra cualquier otro mensaje que no sea la lista.
- **Resiliencia**: Aunque el servidor se reinicie, el bot recupera el estado buscando el mensaje fijado 📌.
- **Privacidad**: Solo los usuarios autorizados en el archivo de configuración (`AUTHORIZED_USERS`) pueden interactuar.

---

<div align="center">
  <sub>Proyecto de Código Abierto diseñado para simplificar el hogar.</sub>
</div>
