from django.conf import settings
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)

_bot_instance = None


def get_bot():
    global _bot_instance
    
    if _bot_instance is None:
        try:
            token = getattr(settings, 'BOT_TOKEN', None)
            if not token:
                raise ValueError("BOT_TOKEN settings.py da topilmadi yoki .env faylida o'rnatilmagan")
            
            _bot_instance = Bot(token=token)
            logger.info("Telegram bot instance created successfully")
        except Exception as e:
            logger.error(f"Failed to create bot instance: {str(e)}")
            raise
    
    return _bot_instance


async def send_message(chat_id, text):
    try:
        bot = get_bot()
        await bot.send_message(chat_id=chat_id, text=text)
        logger.info(f"Message sent to chat_id: {chat_id}")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send message to {chat_id}: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending message: {str(e)}")
        return False
