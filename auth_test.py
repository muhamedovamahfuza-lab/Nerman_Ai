import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerman_ai.settings')
django.setup()

from django.contrib.auth import authenticate
from core.models import User

email = 'javohirqobiljonov32@gmail.com'
password = 'javohir2010007'

print("---AUTHTEST---")
try:
    u = authenticate(email=email, password=password)
    if u:
        print(f"AUTHENTICATED: {u.email}")
        print(f"IS_STAFF: {u.is_staff}")
        print(f"IS_SUPERUSER: {u.is_superuser}")
    else:
        print("AUTHENTICATION_FAILED")
        # Check if user exists but password mismatch
        user_exists = User.objects.filter(email=email).exists()
        print(f"USER_EXISTS_IN_DB: {user_exists}")
        if user_exists:
            u_db = User.objects.get(email=email)
            print(f"DB_USER_STAFF: {u_db.is_staff}")
            print(f"DB_USER_ACTIVE: {u_db.is_active}")
            print(f"DB_USER_SUPER: {u_db.is_superuser}")
except Exception as e:
    print(f"ERROR: {str(e)}")
print("---END---")
