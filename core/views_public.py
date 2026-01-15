from django.shortcuts import render


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


def contact(request):
    """Страница контактов"""
    from .forms import ContactForm
    from django.contrib import messages
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # В production здесь отправка email
            messages.success(request, 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.')
            form = ContactForm()
    else:
        form = ContactForm()
    
    return render(request, 'public/contact.html', {'form': form})
