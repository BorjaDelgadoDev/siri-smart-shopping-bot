import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Tu misión es procesar una lista de productos de la compra de forma profesional y organizada. 
Recibirás un texto crudo que puede contener ruidos como "Añade a la lista", "Dile al bot que...", etc.
Debes limpiar el ruido y devolver ÚNICAMENTE un JSON válido que sea una lista de objetos.

### SECCIONES OBLIGATORIAS:
Debes clasificar CADA producto dentro de UNA de estas secciones exactas (incluye el emoji):
1. 🍏 Frutas y Verduras (ej: tomates, patatas, plátanos)
2. 🥛 Lácteos y Quesos (ej: leche, yogur, queso, mantequilla)
3. 🥩 Carnes y Embutidos (ej: pollo, jamón, salchichas)
4. 🐟 Pescados y Mariscos (ej: merluza, gambas)
5. 🥚 Huevos y Básicos (ej: huevos, aceite, sal, azúcar)
6. 🍞 Panadería y Bollería (ej: pan, magdalenas, galletas)
7. 🍝 Arroces y Pastas (ej: macarrones, arroz, legumbres)
8. 🥫 Conservas y Salsas (ej: tomate frito, atún en lata, mayonesa)
9. 🥤 Bebidas y Cafés (ej: agua, zumo, café, cerveza, vino)
10. 🧻 Limpieza y Hogar (ej: detergente, papel higiénico, lavavajillas)
11. 🧴 Higiene y Cuidado (ej: champú, gel, pasta de dientes)
12. ❄️ Congelados (ej: pizza, helados, verduras congeladas)
13. 📦 Otros (Solo si no encaja en ninguna anterior)

### REGLAS CRÍTICAS:
- "product": El nombre del producto (ej: "Tomates").
- "quantity": La cantidad si se menciona (ej: "3 kilos" o "un pack"), si no, "1".
- "category": Debe ser exactamente una de las 13 anteriores.
- Si el usuario dice "Frutas", clasifícalo en "🍏 Frutas y Verduras".
- Si el usuario dice "Verduras", clasifícalo en "🍏 Frutas y Verduras".

Ejemplo de entrada: "Añade 3 kilos de patatas y un gel de ducha"
Ejemplo de salida: 
[
  {"product": "Patatas", "quantity": "3 kilos", "category": "🍏 Frutas y Verduras"},
  {"product": "Gel de ducha", "quantity": "1", "category": "🧴 Higiene y Cuidado"}
]

NO devuelvas texto adicional, solo el JSON.
"""

def configure_ai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT
    )

def process_text(text):
    model = configure_ai()
    if not model:
        raise ValueError("GEMINI_API_KEY is missing or empty in environment.")
    
    # try/except removido para que main.py capture el error exacto en flight_recorder
    response = model.generate_content(text)
    
    if not response.parts:
        raise ValueError(f"AI returned blocked/empty response. FinishReason: {response.prompt_feedback}")

    raw_content = response.text
    # Limpieza simple por si la IA añade markdown ```json
    clean_response = raw_content.strip().replace("```json", "").replace("```", "")
    
    try:
        data = json.loads(clean_response)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned invalid JSON: {raw_content}")

    if not data:
        raise ValueError(f"AI returned empty list. Raw: {raw_content}")
        
    return data

if __name__ == "__main__":
    # Test simple (no funcionará sin API key real en el entorno)
    print("Testing AI Handler with dummy text...")
    test_text = "Añade huevos y dos kilos de manzanas"
    # Como no hay API Key todavía, esto imprimirá el aviso
    result = process_text(test_text)
    print(f"Result: {result}")
