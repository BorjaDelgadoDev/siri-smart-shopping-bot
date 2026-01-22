from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import ai_handler
import database

load_dotenv()

app = FastAPI(title="Smart Shopping List Bot API")

class SiriRequest(BaseModel):
    text: str

@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Shopping List Bot is running"}

@app.post("/siri")
async def siri_endpoint(request: SiriRequest, x_auth_token: str = Header(None)):
    expected_token = os.getenv("SIRI_AUTH_TOKEN")
    
    # Validación de seguridad
    if not expected_token or x_auth_token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Procesamiento asíncrono (conceptualmente, para que Siri no espere demasiado)
    # Por ahora procesamos y guardamos antes de responder, si Gemini es rápido
    raw_text = request.text
    print(f"Received from Siri: {raw_text}")
    
    products = ai_handler.process_text(raw_text)
    
    for item in products:
        name = item.get("product")
        quantity = item.get("quantity", "1")
        category = item.get("category", "Otros 📦")
        
        if name:
            database.add_item(name, quantity, category)
            print(f"Added item: {name} ({quantity}) in {category}")

    return {"status": "success", "added": len(products)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
