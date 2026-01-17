from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum
import uuid
from .models import User, Chat, Message, APIKey, Invoice, UsageHistory
from .forms import ProfileUpdateForm
from .ai_service import AIService


@login_required
def dashboard(request):
    """Главная страница dashboard - перенаправляет на AI чат"""
    # Перенаправляем на AI чат интерфейс
    return redirect('ai_tasks')


@login_required
def profile_view(request):
    """Профиль и настройки"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'dashboard/profile.html', {'form': form})


@login_required
def subscription_view(request):
    """Управление подпиской"""
    plans = [
        {'name': 'Free', 'price': '0', 'tokens': '1,000'},
        {'name': 'Pro', 'price': '$29', 'tokens': '50,000'},
        {'name': 'Enterprise', 'price': 'Custom', 'tokens': 'Unlimited'}
    ]
    return render(request, 'dashboard/subscription.html', {'plans': plans})


@login_required
def history_view(request):
    """История использования"""
    history = request.user.usage_history.all()
    return render(request, 'dashboard/history.html', {'history': history})


@login_required
def integrations_view(request):
    """API интеграции"""
    if request.method == 'POST':
        name = request.POST.get('name', f'API Key {request.user.api_keys.count() + 1}')
        APIKey.objects.create(user=request.user, name=name)
        messages.success(request, 'API ключ создан!')
        return redirect('integrations')
    
    api_keys = request.user.api_keys.all()
    return render(request, 'dashboard/integrations.html', {'api_keys': api_keys})


@login_required
def billing_view(request):
    """Счета и оплата"""
    invoices = request.user.invoices.all()
    return render(request, 'dashboard/billing.html', {'invoices': invoices})


@login_required
def ai_tasks_view(request):
    """AI чат панель"""
    chats = request.user.chats.all()
    active_chat = None
    
    if chats.exists():
        chat_id = request.GET.get('chat')
        if chat_id:
            active_chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        else:
            active_chat = chats.first()
    
    return render(request, 'dashboard/ai_tasks.html', {
        'chats': chats,
        'active_chat': active_chat
    })


@login_required
@require_POST
def create_chat(request):
    """Создать новый чат"""
    chat = Chat.objects.create(
        user=request.user,
        title=f'Новый чат {request.user.chats.count() + 1}'
    )
    return redirect(f'/dashboard/ai-tasks/?chat={chat.id}')


@login_required
@require_POST
def delete_chat(request, chat_id):
    """Удалить чат"""
    chat = get_object_or_404(Chat, id=chat_id, user=request.user)
    chat.delete()
    messages.success(request, 'Чат удален')
    return redirect('ai_tasks')


@login_required
@require_POST
def send_message(request):
    """Отправить сообщение в AI чат (AJAX)"""
    try:
        chat_id = request.POST.get('chat_id')
        message_text = request.POST.get('message')
        
        if not chat_id or not message_text:
            return JsonResponse({'error': 'Chat ID va xabar majburiy'}, status=400)
        
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)
        
        # Check if user has tokens (minimum 10 tokens required)
        if request.user.tokens < 10:
            return JsonResponse({
                'error': 'Tokenlar yetarli emas! Iltimos, tokenlar sotib oling.',
                'remaining_tokens': request.user.tokens
            }, status=400)
        
        # Сохраняем сообщение пользователя
        user_message = Message.objects.create(
            chat=chat,
            role='user',
            content=message_text
        )
        
        # Обновляем название чата если это первое сообщение
        if chat.messages.count() == 1:
            chat.title = message_text[:50] + ('...' if len(message_text) > 50 else '')
            chat.save()
        
        # Получаем тип сообщения (text yoki image)
        msg_type = request.POST.get('type', 'text')
        
        # Получаем ответ от AI
        ai_service = AIService()
        
        if msg_type == 'image':
            # Rasm generatsiya qilish
            # Image generation costs usually higher, e.g., 50 tokens
            if request.user.tokens < 50:
                 return JsonResponse({
                    'error': 'Rasm chizish uchun kamida 50 token kerak!',
                    'remaining_tokens': request.user.tokens
                }, status=400)

            result = ai_service.generate_image(message_text)
            
            if 'error' in result:
                 return JsonResponse({'error': result['error'], 'success': False})
            
            response_content = f"![Generated Image]({result['image_url']})\n\nPrompt: {result.get('revised_prompt', message_text)}"
            tokens_cost = 50 # Fixed cost for image
            
            # Save AI message with image URL
            ai_message = Message.objects.create(
                chat=chat,
                role='assistant',
                content=response_content,
                tokens_used=tokens_cost
            )
            
            # Deduct tokens
            request.user.tokens -= tokens_cost
            request.user.save()
            
            # Record history
            UsageHistory.objects.create(
                user=request.user,
                action=f'AI Image: {message_text[:30]}...',
                tokens_used=tokens_cost
            )
            
            return JsonResponse({
                'success': True,
                'response': response_content,
                'tokens_used': tokens_cost,
                'remaining_tokens': request.user.tokens,
                'is_image': True,
                'image_url': result['image_url']
            })

        else:
            # TEXT CHAT LOGIC (Existing)
            result = ai_service.send_message(message_text)
            
            # Check if AI service returned an error
            if result['tokens_used'] == 0 and ('xatolik' in result['response'].lower() or '❌' in result['response']):
                # AI service error - still save the error message
                ai_message = Message.objects.create(
                    chat=chat,
                    role='assistant',
                    content=result['response'],
                    tokens_used=0
                )
                return JsonResponse({
                    'success': False,
                    'response': result['response'],
                    'tokens_used': 0,
                    'remaining_tokens': request.user.tokens
                })
            
            # Сохраняем ответ AI
            ai_message = Message.objects.create(
                chat=chat,
                role='assistant',
                content=result['response'],
                tokens_used=result['tokens_used']
            )
            
            # Списываем токены с пользователя
            if result['tokens_used'] > 0:
                request.user.tokens -= result['tokens_used']
                request.user.save()
                
                # Записываем в историю
                UsageHistory.objects.create(
                    user=request.user,
                    action=f'AI Chat: {message_text[:50]}...',
                    tokens_used=result['tokens_used']
                )
            
            return JsonResponse({
                'success': True,
                'response': result['response'],
                'tokens_used': result['tokens_used'],
                'remaining_tokens': request.user.tokens
            })
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in send_message: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'error': f'Xatolik yuz berdi: {str(e)}',
            'success': False
        }, status=500)


@login_required
def tokens_view(request):
    """Управление токенами"""
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        bonus = int(request.POST.get('bonus', 0))
        request.user.tokens += (amount + bonus)
        request.user.save()
        messages.success(request, f'Куплено {amount + bonus} токенов!')
        return redirect('tokens')
    
    packages = [
        {'tokens': 5000, 'price': '$5', 'bonus': 0},
        {'tokens': 15000, 'price': '$14', 'bonus': 1000},
        {'tokens': 50000, 'price': '$45', 'bonus': 5000}
    ]
    return render(request, 'dashboard/tokens.html', {'packages': packages})
