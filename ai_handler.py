import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
Tu misión es procesar una lista de productos de la compra. 
Recibirás un texto crudo que puede contener ruidos como "Añade a la lista", "Dile al bot que...", etc.
Debes limpiar el ruido y devolver ÚNICAMENTE un JSON válido que sea una lista de objetos.
Cada objeto debe tener:
- "product": El nombre del producto (ej: "Leche").
- "quantity": La cantidad si se menciona, si no, "1".
- "category": Una categoría lógica con un emoji (ej: "🥛 Lácteos", "🍏 Frutas", "🥩 Carnes", "🧻 Limpieza", "📦 Otros").

Si no puedes determinar la categoría, usa "📦 Otros".
Si no hay productos claros, devuelve una lista vacía [].

Ejemplo de entrada: "Añade tres cartones de leche y un poco de detergente para platos"
Ejemplo de salida: 
[
  {"product": "Leche", "quantity": "3 cartones", "category": "🥛 Lácteos"},
  {"product": "Detergente de platos", "quantity": "1", "category": "🧻 Limpieza"}
]

NO devuelvas texto adicional, solo el JSON.
"""

def configure_ai():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=SYSTEM_PROMPT
    )

def process_text(text):
    model = configure_ai()
    if not model:
        # Fallback si no hay API Key (para pruebas de estructura)
        print("Warning: GEMINI_API_KEY not found. Returning empty list.")
        return []
    
    try:
        response = model.generate_content(text)
        # Limpieza simple por si la IA añade markdown ```json
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_response)
    except Exception as e:
        print(f"Error processing AI: {e}")
        return []

if __name__ == "__main__":
    # Test simple (no funcionará sin API key real en el entorno)
    print("Testing AI Handler with dummy text...")
    test_text = "Añade huevos y dos kilos de manzanas"
    # Como no hay API Key todavía, esto imprimirá el aviso
    result = process_text(test_text)
    print(f"Result: {result}")
