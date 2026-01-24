# Deployment Safeguards Rule

## Objetivo
Prevenir errores de ejecución y fallos en el despliegue de Render/Railway asegurando que el entorno de producción sea siempre accesible y estable.

## Verificaciones Obligatorias (Pre-Push)

### 1. Configuración del Servidor (Uvicorn)
- **Host**: Siempre debe ser `0.0.0.0` en producción. `127.0.0.1` solo se permite para pruebas locales aisladas.
- **Port**: El puerto debe obtenerse de la variable de entorno `PORT` con un fallback (ej: `int(os.getenv("PORT", 8000))`).
- **Variables**: Asegurar que todass las variables usadas en el `startup_event` o en el bloque `if __name__ == "__main__":` están definidas previamente.

### 2. Integridad del Código
- **Sintaxis**: Ejecutar `ruff check .` o un linter equivalente antes de subir cambios.
- **Dependencies**: Cualquier nueva librería importada debe estar en `requirements.txt`.
- **Environment**: No eliminar variables de entorno críticas (`TELEGRAM_TOKEN`, etc.) sin actualizar el `README.md` y las configuraciones de Render.

### 3. Seguridad
- **Tokens**: No subir NUNCA el archivo `.env`.
- **Debug Endpoints**: Cualquier endpoint de diagnóstico debe estar protegido por un token de acceso consistente con el de Siri.

## Procedimiento ante Fallos
Si un despliegue falla en Render:
1. Revisar inmediatamente los logs de Render para identificar excepciones de Python.
2. Verificar si el host es accesible externamente.
3. Comprobar si hay errores de indentación o variables no definidas.
