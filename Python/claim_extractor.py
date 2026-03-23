import os
import logging
from typing import List
import langextract as lx
import langextract.data 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaimExtractor:
    
    def __init__(self, api_key: str = None):
        self.api_key = (
            api_key or 
            os.getenv('GEMINI_API_KEY') or 
            os.getenv('GOOGLE_API_KEY')
        )
        
        if not self.api_key:
            raise ValueError("❌ API ключ не найден! Вставьте его в код или установите переменную окружения.")
        
        logger.info("✓ ClaimExtractor готов")
    
    def extract(self, text: str) -> List[str]:
        
        prompt = """
        Extract all verifiable claims and facts from the text.
        Split complex sentences into simple facts.
        """
        examples = [
            lx.data.ExampleData(
                text="Moscow is the capital of Russia with 12 million people.",
                extractions=[
                    lx.data.Extraction(
                        extraction_class="claim",
                        extraction_text="Moscow is the capital of Russia",
                        attributes={"fact": "Moscow is the capital of Russia"}
                    ),
                    lx.data.Extraction(
                        extraction_class="claim",
                        extraction_text="12 million people",
                        attributes={"fact": "Population of Moscow is 12 million"}
                    )
                ]
            )
        ]
        
        try:
            results = lx.extract(
                text_or_documents=text,
                prompt_description=prompt,
                examples=examples,
                model_id="gemini-3-flash-preview", 
                api_key=self.api_key
            )
            
            claims = []

            if not isinstance(results, (list, tuple)) and not hasattr(results, '__iter__'):
                results = [results]

            for res in results:
                if hasattr(res, 'extractions') and res.extractions:
                    for item in res.extractions:
                        val = None
                        if item.attributes and 'fact' in item.attributes:
                            val = item.attributes['fact']
                        else:
                            val = item.extraction_text
                        
                        if val:
                            claims.append(val)
            
            return list(set(claims))

        except Exception as e:
            logger.error(f"Ошибка при работе LangExtract: {e}")
            return []

# Функция для быстрого вызова
def extract_claims(text: str, api_key: str = None) -> List[str]:
    return ClaimExtractor(api_key).extract(text)

if __name__ == "__main__":
    extractor = ClaimExtractor()
    
    test_text = "Japan is an island country in East Asia. Its capital is Tokyo."
    print(f"--- Анализ текста ---\n{test_text}\n")
    
    try:
        res = extractor.extract(test_text)
        print(f"✓ Найдено {len(res)} фактов:")
        for i, c in enumerate(res, 1):
            print(f"{i}. {c}")
    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")