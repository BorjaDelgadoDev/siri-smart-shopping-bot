# Política de Seguridad

Este documento describe las prácticas de seguridad y cómo reportar vulnerabilidades.

## 🔐 Manejo de Secretos

- **NUNCA** subas el archivo `.env` al control de versiones.
- Si sospechas que tus tokens (`TELEGRAM_TOKEN`, `GEMINI_API_KEY`, etc.) han sido expuestos, **REVÓCALOS INMEDIATAMENTE** en las plataformas correspondientes (BotFather, Google Cloud).
- Usa el archivo `.env.example` como plantilla para tus configuraciones locales.

## 🌐 Despliegue Seguro

- Al desplegar en servicios como **Render** o **Railway**, usa las configuraciones de variables de entorno de la plataforma en lugar de archivos `.env`.
- El endpoint `/debug/status` está protegido por el mismo token que Siri. Asegúrate de que sea una clave robusta.

## 🛡️ Reporte de Vulnerabilidades

Si encuentras un fallo de seguridad, por favor abre un *Issue* privado o contacta directamente con el desarrollador. No publiques detalles de exploits en issues públicos.
