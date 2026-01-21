from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import SupportTicket, SupportMessage


# Публичные страницы
def home(request):
    """Главная страница"""
    return render(request, 'public/home.html')


def product(request):
    """Страница о продукте"""
    return render(request, 'public/product.html')


def pricing(request):
    """Страница тарифов"""
    plans = [
        {
            'name': 'Free',
            'price': '0',
            'tokens': '1,000',
            'features': ['Basic AI Tasks', '1000 tokens/month', 'Email support']
        },
        {
            'name': 'Pro',
            'price': '$29',
            'tokens': '50,000',
            'features': ['All AI features', '50,000 tokens/month', 'Priority support', 'API access'],
            'highlighted': True
        },
        {
            'name': 'Enterprise',
            'price': 'Custom',
            'tokens': 'Unlimited',
            'features': ['All Pro features', 'Unlimited tokens', 'Dedicated support', 'Custom integrations']
        }
    ]
    return render(request, 'public/pricing.html', {'plans': plans})


def about(request):
    """Страница О нас"""
    return render(request, 'public/about.html')


def faq(request):
    """Страница FAQ"""
    faqs = [
        {
            'question': 'Что такое NERMAN.AI?',
            'answer': 'NERMAN.AI - это платформа искусственного интеллекта для автоматизации бизнес-процессов и решения сложных задач с помощью передовых AI-моделей.'
        },
        {
            'question': 'Как начать использовать платформу?',
            'answer': 'Зарегистрируйтесь бесплатно, получите 1000 стартовых токенов и начните использовать AI для решения ваших задач.'
        },
        {
            'question': 'Что такое токены?',
            'answer': 'Токены - это единицы измерения использования AI. Каждый запрос к AI потребляет определенное количество токенов в зависимости от сложности задачи.'
        },
        {
            'question': 'Безопасны ли мои данные?',
            'answer': 'Абсолютно. Мы используем шифрование данных, соответствуем требованиям GDPR. Ваши данные никогда не передаются третьим лицам.'
        }
    ]
    return render(request, 'public/faq.html', {'faqs': faqs})


def blog(request):
    """Страница блога"""
    posts = [
        {
            'title': 'Как AI меняет бизнес-процессы в 2026',
            'excerpt': 'Искусственный интеллект революционизирует способы работы компаний по всему миру...',
            'author': 'Команда NERMAN.AI',
            'date': '2026-01-10'
        },
        {
            'title': 'Топ-5 способов автоматизации с помощью AI',
            'excerpt': 'Узнайте, какие процессы можно автоматизировать прямо сейчас...',
            'author': 'Команда NERMAN.AI',
            'date': '2026-01-05'
        }
    ]
    return render(request, 'public/blog.html', {'posts': posts})


@login_required
def contact(request):
    """Страница службы поддержки (Чат)"""
    ticket, created = SupportTicket.objects.get_or_create(
        user=request.user,
        status__in=[SupportTicket.Status.OPEN, SupportTicket.Status.IN_PROGRESS],
        defaults={'subject': 'Chat Support'}
    )
    
    if created:
        # Авто-ответ при создании тикета
        SupportMessage.objects.create(
            ticket=ticket,
            sender=SupportMessage.Sender.SUPPORT,
            content="Здравствуйте! Чем я могу помочь вам сегодня?"
        )
    
    messages = ticket.messages.all()
    return render(request, 'public/contact.html', {
        'ticket': ticket,
        'chat_messages': messages
    })


@login_required
def send_support_message(request):
    """AJAX endpoint для отправки сообщения"""
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        content = data.get('content')
        ticket_id = data.get('ticket_id')
        
        ticket = get_object_with_404(SupportTicket, id=ticket_id, user=request.user)
        
        # Сохраняем сообщение пользователя
        message = SupportMessage.objects.create(
            ticket=ticket,
            sender=SupportMessage.Sender.USER,
            content=content
        )
        
        # Имитация авто-ответа (Auto-reply)
        auto_reply_content = ""
        if "привет" in content.lower() or "hello" in content.lower():
            auto_reply_content = "Привет! Я бот поддержки NERMAN.AI. Могу подсказать по тарифам или функциям редактора."
        elif "цена" in content.lower() or "price" in content.lower():
            auto_reply_content = "Наши тарифы начинаются от $0. Вы можете посмотреть подробности на странице 'Подписка'."
        else:
            auto_reply_content = "Ваше сообщение получено. Наши специалисты ответят вам в ближайшее время."
            
        if auto_reply_content:
            SupportMessage.objects.create(
                ticket=ticket,
                sender=SupportMessage.Sender.SUPPORT,
                content=auto_reply_content
            )

        return JsonResponse({
            'status': 'success',
            'message': {
                'content': message.content,
                'timestamp': message.timestamp.strftime('%H:%M'),
                'sender': message.sender
            },
            'auto_reply': {
                'content': auto_reply_content,
                'sender': 'support'
            } if auto_reply_content else None
        })
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def get_support_messages(request, ticket_id):
    """AJAX endpoint для получения новых сообщений (polling)"""
    ticket = get_object_with_404(SupportTicket, id=ticket_id, user=request.user)
    last_id = request.GET.get('last_id', 0)
    
    messages = ticket.messages.filter(id__gt=last_id)
    
    return JsonResponse({
        'messages': [{
            'id': m.id,
            'content': m.content,
            'sender': m.sender,
            'timestamp': m.timestamp.strftime('%H:%M'),
        } for m in messages]
    })


def ai_video_editor(request):
    """Страница ИИ-Видеоредактора (теперь встроена в Product)"""
    return render(request, 'public/product.html')
