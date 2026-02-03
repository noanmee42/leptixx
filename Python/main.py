# Вариант 1
from dotenv import load_dotenv
load_dotenv()  # Загружает .env

from claim_extractor import ClaimExtractor

extractor = ClaimExtractor()  # Теперь найдет ключ
claims = extractor.extract("Япония - большой остров в Тихом океане с населением 125 миллионов человек, основанным в 660 году до н.э.")