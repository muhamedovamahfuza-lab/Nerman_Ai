from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from .models import Subscription


def register_view(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Создаем подписку
            Subscription.objects.create(
                user=user,
                plan='free',
                status='active'
            )
            
            # Автоматический вход (указываем backend явно)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать в NERMAN.AI!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # в нашем случае это email
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user.last_login_time = timezone.now()
                    user.save()
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Ваш аккаунт заблокирован.')
            else:
                messages.error(request, 'Неверный email или пароль.')
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('home')


def password_reset_view(request):
    """Восстановление пароля"""
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.success(request, f'Инструкции по восстановлению пароля отправлены на {email}')
    
    return render(request, 'auth/reset_password.html')
