---
name: sdd-manager
description: Gestiona el desarrollo siguiendo la metodología Spec-Driven Development (SDD). Úsalo para asegurar que el código cumple con las especificaciones y el roadmap.
---

# SDD Manager Skill

## Objetivo
Guiar al agente para desarrollar el Smart Shopping List Bot basándose estrictamente en los documentos de la carpeta `docs/`.

## Instrucciones de Flujo (SDD)
1. **Pre-vuelo**: Antes de cualquier edición, lee `docs/spec.md` y `docs/plan.md`.
2. **Ejecución**: Identifica la primera tarea pendiente en `docs/tasks.md`.
3. **Verificación**: Tras escribir código, verifica que:
   - Los productos se agrupan por categorías (IA Gemini).
   - Se usa `editMessageText` para el Mensaje Maestro (Telegram).
   - El coste es 0€ (SQLite + Capas gratuitas).
4. **Cierre**: Marca la tarea con [x] en `docs/tasks.md` antes de terminar la sesión.

## Restricciones Innegociables
- No hardcodear API Keys (usar `os.getenv`).
- No generar mensajes nuevos si existe un `master_message_id`.