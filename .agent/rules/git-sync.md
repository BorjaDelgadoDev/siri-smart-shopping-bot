# Reglas de Git y GitHub (gh)

Esta regla asegura que el asistente mantenga siempre el repositorio sincronizado y utilice las herramientas disponibles para verificar el estado remoto.

## 🚀 Flujo de Trabajo Obligatorio

1.  **Sin Cambios Pendientes**: Antes de finalizar cualquier tarea que implique modificar código, DEBES verificar que no queden cambios en el `staged` o `unstaged` (`git status`).
2.  **Commit Automático**: Si has realizado cambios funcionales, SIEMPRE debes realizar un `git commit` con un mensaje descriptivo siguiendo el estándar de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
3.  **Verificación Pre-Sincronización**: Antes de hacer `push`, DEBES verificar que el código sea correcto. Esto incluye:
    *   Ejecutar tests si están disponibles.
    *   Verificar sintaxis (ej: `python3 -m py_compile *.py`).
    *   Asegurar que no hay secretos expuestos accidentalmente.
4.  **Sincronización Remota**: Una vez verificado, debes realizar un `git push`.
4.  **Uso de `gh` CLI**: Tienes permiso y capacidad para usar `gh` (GitHub CLI) para:
    *   Verificar el estado de los PRs o Issues.
    *   Comprobar el estado de las GitHub Actions (si existen).
    *   Verificar la autenticación del usuario.

## 🛑 Prohibiciones

*   **NUNCA** termines una tarea dejando archivos modificados sin comitear.
*   **NUNCA** asumas que el repositorio remoto está actualizado sin hacer un `push` tras los commits.

## 🛠️ Comandos de Verificación
*   `git status` para ver cambios pendientes.
*   `gh auth status` para verificar la conexión con GitHub.
*   `git push origin [rama]` para sincronizar.
