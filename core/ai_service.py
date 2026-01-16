import openai
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    """OpenAI va Google Gemini bilan ishlovchi universal AI servisi"""

    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.api_type = settings.AI_API_TYPE  # settings.py da 'openai' yoki 'gemini' bo'lishi kerak

        if self.api_type == 'gemini' and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        elif self.api_type == 'openai' and self.api_key:
            openai.api_key = self.api_key

    def send_message(self, message: str, chat_history: list = None) -> dict:
        try:
            if not self.api_key:
                return {
                    'response': 'API kalit topilmadi. Iltimos, Render Environment Variables bo\'limiga AI_API_KEY qo\'shing.',
                    'tokens_used': 0
                }

            # --- OPENAI BILAN ISHLASH ---
            if self.api_type == 'openai':
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": message}]
                )
                return {
                    'response': response.choices[0].message.content,
                    'tokens_used': response.usage.total_tokens
                }

            # --- GEMINI BILAN ISHLASH ---
            else:
                response = self.model.generate_content(message)
                tokens_used = (len(message) + len(response.text)) // 4
                return {
                    'response': response.text,
                    'tokens_used': tokens_used
                }

        except Exception as e:
            logger.error(f"AI API Error: {str(e)}")
            return {
                'response': f'AI so\'rovida xatolik: {str(e)}',
                'tokens_used': 0
            }