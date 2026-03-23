

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import json
from datetime import datetime
from pathlib import Path

from claim_extractor import ClaimExtractor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hallucination Detector API",
    description="API для извлечения и верификации утверждений",
    version="1.0.0"
)

try:
    extractor = ClaimExtractor()
    logger.info("✓ ClaimExtractor успешно инициализирован")
except Exception as e:
    logger.error(f"❌ Ошибка инициализации: {e}")
    extractor = None



class ExtractClaimsRequest(BaseModel):
    text: str
    query: str = ""  # Опциональное поле для запроса пользователя
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "Москва - столица России. Население более 12 миллионов.",
                "query": "Столица России?"
            }
        }


class ExtractClaimsResponse(BaseModel):
    claims: List[str]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "claims": [
                    "Москва - столица России",
                    "Население Москвы более 12 миллионов"
                ],
                "count": 2
            }
        }



@app.get("/health")
def health_check():
    """Проверка работоспособности API"""
    return {
        "status": "healthy",
        "extractor_ready": extractor is not None
    }


@app.post("/extract-claims", response_model=ExtractClaimsResponse)
def extract_claims_endpoint(request: ExtractClaimsRequest):
    # Возвращает список утверждений
    if extractor is None:
        raise HTTPException(
            status_code=500,
            detail="ClaimExtractor не инициализирован. Проверьте GEMINI_API_KEY."
        )
    
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Текст не может быть пустым"
        )
    
    try:
        logger.info(f"Извлечение утверждений из текста ({len(request.text)} символов)")
        
        claims = extractor.extract(request.text)
        
        logger.info(f"✓ Извлечено {len(claims)} утверждений")
        
        return ExtractClaimsResponse(claims=claims, count=len(claims))
        
    except Exception as e:
        logger.error(f"Ошибка при извлечении: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки: {str(e)}"
        )


@app.post("/extract-and-save")
def extract_and_save_endpoint(request: ExtractClaimsRequest):
    # Сохраняет в JSON
    if extractor is None:
        raise HTTPException(
            status_code=500,
            detail="ClaimExtractor не инициализирован. Проверьте GEMINI_API_KEY."
        )
    
    if not request.text or not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Текст не может быть пустым"
        )
    
    try:
        # Извлечение утверждений
        logger.info(f"Извлечение утверждений из текста ({len(request.text)} символов)")
        claims = extractor.extract(request.text)
        logger.info(f"✓ Извлечено {len(claims)} утверждений")
        
        # Создание структуры для сохранения
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "query": request.query,
            "response": request.text,
            "claims": claims,
            "count": len(claims)
        }

        output_dir = Path("../output")
        output_dir.mkdir(exist_ok=True)
        
        # Генерация имени файла с датой и временем
        filename = f"claims_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_dir / filename
        
        # Сохранение в JSON файл
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✓ Сохранено в {filepath}")
        
        return {
            "success": True,
            "filename": str(filepath),
            "claims_count": len(claims),
            "claims": claims
        }
        
    except Exception as e:
        logger.error(f"Ошибка при обработке: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обработки: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 Запуск Hallucination Detector API")
    print("=" * 60)
    print(f"📍 URL: http://localhost:8000")
    print(f"📖 Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True, 
        log_level="info"
    )