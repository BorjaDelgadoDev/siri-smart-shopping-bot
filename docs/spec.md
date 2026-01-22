Spec: Sistema de Lista de Compra Inteligente (Low Cost)

1. Visión General

Un sistema de lista de compra compartida para parejas que centraliza la entrada de datos vía voz (Siri) y la gestión visual en un único mensaje "maestro" en Telegram. El sistema opera con coste cero utilizando capas gratuitas de servicios modernos (Gemini, Render, SQLite).

2. Historias de Usuario (User Stories)

Historia 1: Entrada rápida por voz (Siri)

Como usuario, quiero dictar productos a Siri (ej: "Añade huevos, leche y detergente"), para que se registren automáticamente sin abrir la app.

Criterios de Aceptación:

El sistema recibe un JSON con el texto crudo desde un Atajo de iOS.

El texto es procesado por Gemini para limpiar ruidos ("dile al bot que...") y extraer productos, cantidades y categorías.

El sistema confirma la recepción con un código 200 rápido para que Siri no se bloquee.

Historia 2: Interfaz de Mensaje Maestro (Telegram UX)

Como usuario en el supermercado, quiero tener un solo mensaje fijado que se actualice dinámicamente, para evitar el scroll y mensajes basura.

Criterios de Aceptación:

Al añadir un item, el sistema busca el mensaje anterior y lo edita. Solo envía uno nuevo si no existe el anterior.

Los productos se agrupan por categorías con emojis (ej: 🥛 Lácteos, 🍏 Frutas).

Cada producto tiene un botón (inline) para ser marcado como "Comprado", eliminándolo de la lista.

3. Seguridad y Privacidad

Acceso Restringido: Solo los IDs de Telegram autorizados en el archivo .env pueden interactuar.

Autenticación Siri: El endpoint requiere un header X-Auth-Token secreto.

Variables de Entorno: No se permiten claves API hardcodeadas.

4. Casos Borde

Duplicados: Si se añade un producto existente, se ignora o se actualiza.

Fallo de Categoría: Se asigna a "Otros 📦" por defecto.

Persistencia: El ID del mensaje maestro se guarda en la base de datos para recuperarlo tras un reinicio.