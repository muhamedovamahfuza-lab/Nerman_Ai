import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerman_ai.settings')
django.setup()

from core.models import User

email = 'javohirqobiljonov32@gmail.com'
u = User.objects.filter(email=email).first()

print(f"---RESULT---")
if u:
    print(f"Email: {u.email}")
    print(f"Is Staff: {u.is_staff}")
    print(f"Is Superuser: {u.is_superuser}")
    print(f"Is Active: {u.is_active}")
    print(f"Username: {u.username}")
    print(f"Has Password: {u.has_usable_password()}")
else:
    print("User not found")
print(f"---END---")
