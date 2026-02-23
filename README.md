# LEPTIXX

**[🇷🇺 Русский](#русский) | [🇬🇧 English](#english)**

---

## Русский

**leptixx** — CLI-приложение для обнаружения галлюцинаций в ответах нейросетей, разбивая текст на атомарные утверждения.

### Установка через архив

Готовый архив для Windows можно скачать на странице [Releases](https://github.com/noanmee42/leptixx/releases) 

### Установка через репозиторий

**1. Клонируйте репозиторий**
```bash
git clone https://github.com/noanmee42/leptixx.git
cd leptixx
```

**2. Установите зависимости Python**
```bash
cd Python
pip install -r requirements.txt
```

**3. Установите зависимости Go**
```bash
cd Go
go mod download
```

**4. Получите API-ключи**

- **GEMINI_API_KEY**
  1. Перейди на [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
  2. Нажми «Create API key»
  3. Скопируй ключ

- **JINA_API_KEY**
  1. Перейди на [jina.ai](https://jina.ai)
  2. Зарегистрируйся и перейди в раздел API
  3. Скопируй ключ

**5. Установите переменные окружения**

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="твой_ключ"
$env:JINA_API_KEY="твой_ключ"
```

Windows (CMD):
```cmd
set GEMINI_API_KEY=твой_ключ
set JINA_API_KEY=твой_ключ
```

Linux / macOS:
```bash
export GEMINI_API_KEY=твой_ключ
export JINA_API_KEY=твой_ключ
```

**6. Запустите приложение**
```bash
cd ..
go run ./Go/
```

Python-сервер запустится автоматически. Если этого не произошло — запусти вручную в отдельном терминале:
```bash
cd Python
python app.py
```

---

### Команды

| Команда | Описание |
|---|---|
| `/check -r "текст"` | Извлечь утверждения из текста и проверить каждое на достоверность |
| `/verify` | Проверить, установлены ли API-ключи и запущен ли Python-сервер |
| `/help` | Показать список команд |
| `/exit` | Выйти из приложения |


### Лицензия

Распространяется под лицензией MIT (см. "MIT License")

---

## English

**leptixx** — a CLI application for detecting hallucinations in AI responses. It splits text into atomic claims.

### Download archive

A ready-to-use archive for Windows is available on the [Releases](https://github.com/noanmee42/leptixx/releases) page.

### Requirements

**1. Clone the repository**
```bash
git clone https://github.com/noanmee42/leptixx.git
cd leptixx
```

**2. Install Python dependencies**
```bash
cd Python
pip install -r requirements.txt
```

**3. Install Go dependencies**
```bash
cd Go
go mod download
```

**4. Get API keys**

- **GEMINI_API_KEY**
  1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
  2. Click «Create API key»
  3. Copy the key

- **JINA_API_KEY** 
  1. Go to [jina.ai](https://jina.ai)
  2. Register and navigate to the API section
  3. Copy the key

**5. Set environment variables**

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_key"
$env:JINA_API_KEY="your_key"
```

Windows (CMD):
```cmd
set GEMINI_API_KEY=your_key
set JINA_API_KEY=your_key
```

Linux / macOS:
```bash
export GEMINI_API_KEY=your_key
export JINA_API_KEY=your_key
```

**6. Run the application**
```bash
cd ..
go run ./Go/
```

The Python server starts automatically. If it doesn't, run it manually in a separate terminal:
```bash
cd Python
python app.py
```

---

### Commands

| Command | Description |
|---|---|
| `/check -r "text"` | Extract claims from text and verify each one |
| `/verify` | Check if API keys are set and the Python server is running |
| `/help` | Show the list of commands |
| `/exit` | Exit the application |

### License

See the "MIT License" tab.