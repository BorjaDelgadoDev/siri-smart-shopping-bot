# Smart Shopping List Bot

Bot inteligente para gestionar listas de compra mediante Siri y Telegram. Utiliza Google Gemini para categorizar productos automáticamente.

## ✨ Características

- **Dictado por Voz**: Añade productos usando Siri desde tu iPhone.
- **Categorización Inteligente**: La IA agrupa los productos (Frutería, Lácteos, etc.) con emojis.
- **Mensaje Maestro**: Un único mensaje fijado en Telegram que se actualiza dinámicamente.
- **Modo Conserje**: Limpieza automática de mensajes extra en el grupo.

## 🚀 Instalación Rápida

1. **Clonar el repo**:
   ```bash
   git clone https://github.com/BorjaDelgadoDev/chatboot-telegram.git
   cd chatboot-telegram
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables**:
   Copia `.env.example` a `.env` y rellena tus claves.

4. **Ejecutar**:
   ```bash
   python main.py
   ```

## 🔒 Seguridad

- El acceso al API está protegido por un token de autorización (`X-Auth-Token`).
- No compartas tu archivo `.env` ni lo subas a repositorios públicos.
- Consulta [SECURITY.md](./SECURITY.md) para más detalles.

## 🛠️ Tecnologías

- **FastAPI**: Backend de alto rendimiento.
- **python-telegram-bot**: Interfaz con Telegram.
- **Google Generative AI**: Procesamiento de lenguaje natural (Gemini).
- **SQLite**: Persistencia local de datos.
