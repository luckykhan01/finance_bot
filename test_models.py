import google.genai as genai
from app.core.config import settings
import asyncio

genai.Client(api_key=settings.GEMINI_API_KEY)

MODEL_ID = 'gemini-2.5-flash'

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)