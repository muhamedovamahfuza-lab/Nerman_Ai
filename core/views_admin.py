from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from .models import User


def is_admin(user):
    """Проверка что пользователь админ"""
    return user.is_authenticated and user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def admin_users_view(request):
    """Управление пользователями (только для админов)"""
    users = User.objects.all().annotate(
        chats_count=Count('chats')
    ).order_by('-date_joined')
    
    # Статистика
    total_users = users.count()
    active_users = users.filter(is_active=True).count()
    admin_users = users.filter(role='admin').count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'active_users': active_users,
        'admin_users': admin_users
    }
    
    return render(request, 'admin/users.html', context)


@login_required
@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    """Блокировка/разблокировка пользователя"""
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        
        status = 'активирован' if user.is_active else 'заблокирован'
        messages.success(request, f'Пользователь {user.email} {status}')
    
    return redirect('admin_users')


@login_required
@user_passes_test(is_admin)
def change_user_role(request, user_id):
    """Изменение роли пользователя"""
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        new_role = request.POST.get('role')
        
        if new_role in ['user', 'admin', 'support']:
            user.role = new_role
            user.save()
            messages.success(request, f'Роль пользователя {user.email} изменена на {new_role}')
    
    return redirect('admin_users')
