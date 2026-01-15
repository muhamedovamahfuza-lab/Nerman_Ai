from django.urls import path
from . import views_public, views_auth, views_dashboard, views_admin

urlpatterns = [
    # Публичные страницы
    path('', views_public.home, name='home'),
    path('product/', views_public.product, name='product'),
    path('pricing/', views_public.pricing, name='pricing'),
    path('about/', views_public.about, name='about'),
    path('faq/', views_public.faq, name='faq'),
    path('blog/', views_public.blog, name='blog'),
    path('contact/', views_public.contact, name='contact'),
    
    # Аутентификация
    path('auth/register/', views_auth.register_view, name='register'),
    path('auth/login/', views_auth.login_view, name='login'),
    path('auth/logout/', views_auth.logout_view, name='logout'),
    path('auth/reset-password/', views_auth.password_reset_view, name='reset_password'),
    
    # Dashboard
    path('dashboard/', views_dashboard.dashboard, name='dashboard'),
    path('dashboard/profile/', views_dashboard.profile_view, name='profile'),
    path('dashboard/subscription/', views_dashboard.subscription_view, name='subscription'),
    path('dashboard/history/', views_dashboard.history_view, name='history'),
    path('dashboard/integrations/', views_dashboard.integrations_view, name='integrations'),
    path('dashboard/billing/', views_dashboard.billing_view, name='billing'),
    path('dashboard/ai-tasks/', views_dashboard.ai_tasks_view, name='ai_tasks'),
    path('dashboard/tokens/', views_dashboard.tokens_view, name='tokens'),
    
    # AI Chat AJAX
    path('api/chat/create/', views_dashboard.create_chat, name='create_chat'),
    path('api/chat/<int:chat_id>/delete/', views_dashboard.delete_chat, name='delete_chat'),
    path('api/chat/send/', views_dashboard.send_message, name='send_message'),
    
    # Admin
    path('admin-panel/users/', views_admin.admin_users_view, name='admin_users'),
    path('admin-panel/users/<int:user_id>/toggle/', views_admin.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/users/<int:user_id>/role/', views_admin.change_user_role, name='change_user_role'),
]
