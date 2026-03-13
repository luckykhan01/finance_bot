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
        1. account_name: Определи счет. "каспи" -> "Kaspi", "фридом" -> "Freedom" и т.д. Если счет не указан явно, попробуй угадать, но лучше использовать стандартные названия.
        2. amount: Вытащи сумму (всегда положительное число, типа float).
        3. t_type: "expense" (расход) или "income" (доход).
        4. category: Краткая категория ("Еда", "Такси", "Подарки", "Переводы").
        5. description: Место транзакции или контекст (например: "Магнум", "KFC", "Скинул брату на ДР", "За интернет"). Если контекста нет, верни пустую строку "".

        Верни ТОЛЬКО валидный JSON.

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