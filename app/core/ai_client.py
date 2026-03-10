import json
from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL_ID = 'gemini-2.5-flash'

async def parse_transaction_text(text: str) -> dict:
    """Sends text to Gemini and gets structured dict()"""
    prompt = f"""
    Ты умный финансовый ассистент. Твоя задача — извлечь данные о транзакции из текста пользователя.
    
    Правила:
    1. account_name: Определи банк или счет. "каспи" -> "Kaspi", "фридом" -> "Freedom", "наличка" -> "Cash". По умолчанию ставь "Kaspi".
    2. amount: Вытащи сумму (всегда положительное число, типа float).
    3. t_type: Если есть знак минус, слова "купил", "потратил", "еда" -> "expense". Если плюс, "зарплата", "перевели" -> "income".
    4. category: Кратко определи категорию и напиши её СТРОГО НА АНГЛИЙСКОМ ЯЗЫКЕ (например: "Food", "Transport", "Salary", "Entertainment"), даже если пользователь пишет на русском.
    5. description: Оригинальный текст или краткое пояснение.
    
    Верни ТОЛЬКО валидный JSON без маркдауна, бэктиков (```) и лишнего текста.
    
    Формат ответа строго:
    {{
        "account_name": "string",
        "amount": 0.0,
        "t_type": "income" | "expense",
        "category": "string",
        "description": "string"
    }}
    
    Текст пользователя: "{text}"
    """

    try:
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )

        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Parsing Error {e}")
        print(None)