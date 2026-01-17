import openai
from openai import OpenAI
import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIService:
    """OpenAI va Google Gemini bilan ishlovchi universal AI servisi"""

    def __init__(self):
        # Get API configuration from Django settings
        self.api_key = settings.AI_API_KEY
        self.api_type = settings.AI_API_TYPE
        self.openai_client = None
        
        # Log configuration status (without exposing the key)
        if self.api_key:
            logger.info(f"AI Service initialized with {self.api_type} API (key present)")
        else:
            logger.warning(f"AI Service initialized but API key is missing! Check environment variable AI_API_KEY")

        # Configure AI service based on type
        try:
            if self.api_type == 'gemini' and self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini AI model configured successfully")
            elif self.api_type == 'openai' and self.api_key:
                # Use explicit client instantiation for OpenAI v1+
                self.openai_client = OpenAI(api_key=self.api_key)
                logger.info("OpenAI client configured successfully")
            elif not self.api_key:
                logger.warning(f"Cannot configure {self.api_type} - API key is missing")
            else:
                logger.warning(f"Unknown AI_API_TYPE: {self.api_type}")
        except Exception as e:
            logger.error(f"Failed to initialize {self.api_type} API: {str(e)}", exc_info=True)

    def send_message(self, message: str, chat_history: list = None) -> dict:
        """Send message to AI and get response with improved error handling"""
        
        # Check if API key exists
        if not self.api_key:
            logger.warning("AI API key not configured")
            return {
                'response': 'API kalit topilmadi. Iltimos, .env faylida AI_API_KEY sozlang yoki administratorga murojaat qiling.',
                'tokens_used': 0
            }

        try:
            # --- OPENAI BILAN ISHLASH ---
            if self.api_type == 'openai':
                if not self.openai_client:
                    # Try to initialize if not already done
                    self.openai_client = OpenAI(api_key=self.api_key)

                try:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": message}],
                        max_tokens=500  # Limit response length
                    )
                    return {
                        'response': response.choices[0].message.content,
                        'tokens_used': response.usage.total_tokens
                    }
                except openai.AuthenticationError:
                    logger.error("OpenAI authentication failed - invalid API key")
                    return {
                        'response': '❌ Autentifikatsiya xatosi: OpenAI API kaliti noto\'g\'ri yoki yaroqsiz. Iltimos, yangi API kalit oling.',
                        'tokens_used': 0
                    }
                except openai.RateLimitError:
                    logger.error("OpenAI rate limit or quota exceeded")
                    return {
                        'response': '⚠️ Limitdan oshdi yoki hisobda mablag\' yetarli emas. Iltimos, OpenAI hisobingizni tekshiring (Quota/Billing).',
                        'tokens_used': 0
                    }
                except openai.APIError as e:
                    logger.error(f"OpenAI API error: {str(e)}")
                    return {
                        'response': f'OpenAI API xatosi: {str(e)}. Iltimos, qayta urinib ko\'ring.',
                        'tokens_used': 0
                    }

            # --- GEMINI BILAN ISHLASH ---
            else:
                try:
                    response = self.model.generate_content(message)
                    
                    # Check if response was blocked
                    if not response.text:
                        logger.warning("Gemini response was blocked or empty")
                        return {
                            'response': '⚠️ Javob bloklandi yoki bo\'sh. Iltimos, boshqa savol bering.',
                            'tokens_used': 0
                        }
                    
                    tokens_used = (len(message) + len(response.text)) // 4
                    return {
                        'response': response.text,
                        'tokens_used': tokens_used
                    }
                except Exception as e:
                    error_msg = str(e).lower()
                    if 'api_key' in error_msg or 'authentication' in error_msg:
                        logger.error("Gemini authentication failed")
                        return {
                            'response': '❌ Gemini API kaliti noto\'g\'ri. Iltimos, sozlamalarni tekshiring.',
                            'tokens_used': 0
                        }
                    elif 'quota' in error_msg or 'limit' in error_msg:
                        logger.error("Gemini quota exceeded")
                        return {
                            'response': '⚠️ Gemini limitdan oshdi. Iltimos, kuting yoki boshqa API kalit ishlating.',
                            'tokens_used': 0
                        }
                    else:
                        logger.error(f"Gemini error: {str(e)}")
                        return {
                            'response': f'Gemini xatosi: {str(e)}',
                            'tokens_used': 0
                        }

        except Exception as e:
            # Catch any unexpected errors
            logger.error(f"Unexpected AI service error: {str(e)}", exc_info=True)
    def generate_image(self, prompt: str, size: str = "1024x1024") -> dict:
        """Generate image using DALL-E 3"""
        if not self.api_key:
            return {'error': 'API key not configured'}

        try:
            if self.api_type == 'openai':
                if not self.openai_client:
                    self.openai_client = OpenAI(api_key=self.api_key)

                response = self.openai_client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size=size,
                    quality="standard",
                    n=1,
                )
                return {
                    'image_url': response.data[0].url,
                    'revised_prompt': response.data[0].revised_prompt
                }
            else:
                 return {'error': 'Image generation is currently only supported with OpenAI.'}

        except Exception as e:
            logger.error(f"Image generation error: {str(e)}")
            return {'error': str(e)}
