import os
import sys
import django
from pathlib import Path

# Set up Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nerman_ai.settings')
django.setup()

from django.conf import settings

print("--- VERIFICATION ---")
print(f"AI_API_TYPE: {settings.AI_API_TYPE}")
print(f"AI_API_KEY (last 4): ...{settings.AI_API_KEY[-4:] if settings.AI_API_KEY else 'None'}")
print(f"DEBUG: {settings.DEBUG}")
print("--- END ---")
