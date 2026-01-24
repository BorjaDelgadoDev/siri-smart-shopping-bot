description: Muestra rápidamente el contenido de la lista de la compra del bot. Úsalo también cuando el usuario diga "dime la lista", "dime la lista actual" o similar. 

Cuando el usuario diga "botlista", el agente debe seguir estos pasos:

// turbo
1. Obtener el token de Siri ejecutando: `grep SIRI_AUTH_TOKEN .env | cut -d'=' -f2`
// turbo
2. Consultar el endpoint de auditoría: `curl -s -X GET https://chatboot-telegram.onrender.com/audit -H "X-Auth-Token: <TOKEN>"`
// turbo
3. Consultar el estado detallado para obtener el texto del mensaje fijado: `TOKEN_TG=$(grep TELEGRAM_TOKEN .env | cut -d'=' -f2) && CHAT_ID=$(grep CHAT_ID .env | cut -d'=' -f2) && curl -s "https://api.telegram.org/bot$TOKEN_TG/getChat?chat_id=$CHAT_ID"`
4. Responder al usuario únicamente con un resumen amigable de los productos que hay en la lista, sin detalles técnicos innecesarios, a menos que el usuario los pida.
