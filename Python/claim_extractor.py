import spacy

print("Инициализация ядра. Загрузка spaCy (ru_core_news_sm)...")
try:
    nlp = spacy.load("ru_core_news_sm")
    print("Ядро успешно загружено!")
except OSError:
    print("ОШИБКА: Модель не найдена. Выполните: python -m spacy download ru_core_news_sm")
    exit(1)

def process_text(text: str):
    # Пока что разбивка только на уровне предложений. В будущем будет так же круто как с langextract клянусь
    doc = nlp(text)
    claims = []
    
    for sent in doc.sents:
        cleaned_text = sent.text.strip()
        # Игнорируем слишком короткие фрагменты
        if len(cleaned_text) > 5:
            claims.append(cleaned_text)
            
    return claims