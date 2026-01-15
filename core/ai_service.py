import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    """Сервис для работы с AI API (Google Gemini)"""
    
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.api_type = settings.AI_API_TYPE
        
        if self.api_type == 'gemini' and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def send_message(self, message: str, chat_history: list = None) -> dict:
        """
        Отправить сообщение в AI и получить ответ
        
        Args:
            message: Текст сообщения от пользователя
            chat_history: История чата (опционально)
        
        Returns:
            dict с полями 'response' и 'tokens_used'
        """
        try:
            if not self.api_key or self.api_key == 'your_google_gemini_api_key_here':
                # Возвращаем демо-ответ если API ключ не настроен
                return {
                    'response': f'Это демо-ответ от AI. Ваш запрос: "{message}". \n\nДля полноценной работы добавьте ваш Google Gemini API ключ в файл .env (AI_API_KEY)',
                    'tokens_used': 50
                }
            
            # Отправляем запрос к Gemini
            response = self.model.generate_content(message)
            
            # Приблизительный подсчет токенов (1 токен ≈ 4 символа)
            tokens_used = (len(message) + len(response.text)) // 4
            
            return {
                'response': response.text,
                'tokens_used': tokens_used
            }
            
        except Exception as e:
            logger.error(f"AI API Error: {str(e)}")
            return {
                'response': f'Произошла ошибка при обращении к AI: {str(e)}',
                'tokens_used': 0
            }
    
    def estimate_tokens(self, text: str) -> int:
        """Приблизительная оценка токенов"""
        return len(text) // 4
