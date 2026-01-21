import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerman_ai.settings')
django.setup()

from core.models import User

email = 'test_admin@example.com'
password = 'testpassword123'

print("---TEST_USERMANAGER---")
try:
    # Delete if exists
    User.objects.filter(email=email).delete()
    
    # Test create_superuser
    u = User.objects.create_superuser(
        email=email,
        password=password,
        first_name='Test',
        last_name='Admin'
    )
    print(f"SUCCESS: Created superuser {u.email}")
    print(f"IS_STAFF: {u.is_staff}")
    print(f"IS_SUPERUSER: {u.is_superuser}")
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
print("---END---")
