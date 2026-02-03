# python/claim_extractor.py

import os
import logging
from typing import List

import langextract as lx

logger = logging.getLogger(__name__)


class ClaimExtractor:
    """Извлечение утверждений из текста через langextract + Gemini"""
    
    def __init__(self, api_key: str = None):
        # Поддержка разных способов передачи ключа
        self.api_key = (
            api_key or 
            os.getenv('GEMINI_API_KEY') or 
            os.getenv('GOOGLE_API_KEY')
        )
        
        if not self.api_key:
            raise ValueError(
                "❌ API ключ не найден!\n\n"
                "Способы указать ключ:\n"
                "1. Передайте в конструктор: ClaimExtractor(api_key='ваш_ключ')\n"
                "2. Создайте файл .env с: GEMINI_API_KEY=ваш_ключ\n"
                "3. Установите переменную: export GEMINI_API_KEY=ваш_ключ\n\n"
                "🔑 Получите ключ на: https://aistudio.google.com/app/apikey"
            )
        
        logger.info("✓ ClaimExtractor готов")
    
    def extract(self, text: str) -> List[str]:
        """Извлекает утверждения из текста"""
        
        prompt = """
        Извлеки все проверяемые утверждения из текста.
        Разбей сложные предложения на простые факты.
        Игнорируй вопросы.
        """
        
        examples = [
            {
                "input": "Москва - столица России с населением 12 млн человек.",
                "output": [
                    {"claim": "Москва является столицей России"},
                    {"claim": "Население Москвы составляет 12 миллионов человек"}
                ]
            }
        ]
        
        result = lx.extract(
            text_or_documents=text,
            prompt_description=prompt,
            examples=examples,
            model_id="gemini-2.5-flash",
            api_key=self.api_key  # langextract сам работает с новым API
        )

        # Debugging: Print the structure of the result
        print("DEBUG: Result structure:", result)
        
        # Парсим результат
        claims = []
        try:
            if isinstance(result, dict) and 'extractions' in result:
                claims = [e.get('extraction_text', '').strip() for e in result['extractions'] if 'extraction_text' in e]
            elif isinstance(result, list):
                claims = [item.get('extraction_text', '').strip() if isinstance(item, dict) else str(item) for item in result]
            else:
                logger.error("Unexpected result structure: %s", result)
                claims = []
        except Exception as e:
            logger.error(f"Error parsing extraction result: {e}")
            raise
        
        return [c for c in claims if c and len(c) >= 10]


# Быстрая функция
def extract_claims(text: str, api_key: str = None) -> List[str]:
    return ClaimExtractor(api_key).extract(text)


if __name__ == "__main__":
    # Тест
    extractor = ClaimExtractor()
    
    text = "Москва - столица России. Население более 12 миллионов."
    claims = extractor.extract(text)
    
    print(f"✓ Извлечено {len(claims)} утверждений:")
    for i, claim in enumerate(claims, 1):
        print(f"{i}. {claim}")