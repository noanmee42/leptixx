from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import datetime
import json
import os

from claim_extractor import process_text

app = FastAPI(title="Leptixx NLP")

class TextRequest(BaseModel):
    text: str

# Healthcheck
@app.get("/health")
def healthcheck():
    return {"status": "ok", "service": "spaCy NLP"}

@app.post("/extract-and-save")
def extract_and_save(req: TextRequest):
    try:
        # Получаем факты из нашего модуля
        extracted_claims = process_text(req.text)
        
        # Создаем папку output
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
        os.makedirs(output_dir, exist_ok=True)
        
        # Генерируем таймстемп и имя файла
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(output_dir, f"claims_{timestamp}.json")
        
        # --- ИЗМЕНЕНИЕ ЗДЕСЬ ---
        # Формируем объект данных точно под структуру ClaimsData в Go
        claims_data = {
            "timestamp": timestamp,
            "query": req.text,        # исходный текст
            "response": req.text,     
            "claims": extracted_claims,
            "count": len(extracted_claims)
        }
        
        # Сохраняем в файл сформированный объект (а не просто массив)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(claims_data, f, ensure_ascii=False, indent=2)
            
        # Возвращаем ответ для ExtractSaveResponse
        return {
            "success": True,
            "filename": filename,
            "claims_count": len(extracted_claims),
            "claims": extracted_claims
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)