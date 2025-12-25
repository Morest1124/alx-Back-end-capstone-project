"""
Quick test to verify Django is installed and working.
This script adds the site-packages path explicitly due to Python 3.14.2 import corruption.
"""
import sys
sys.path.insert(0, r'C:\Users\mores\AppData\Local\Programs\pythoncore-3.14-64\Lib\site-packages')

import django
from django.conf import settings
from django.core.management import execute_from_command_line

print("=" * 50)
print("✅ Django is installed and working!")
print("=" * 50)
print(f"Django Version: {django.get_version()}")
print(f"Django Path: {django.__file__}")
print(f"Major.Minor: {django.VERSION[0]}.{django.VERSION[1]}")
print("=" * 50)

# Basic configuration test
settings.configure(
    DEBUG=True,
    SECRET_KEY='test-secret-key-for-verification',
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'django.contrib.auth',
    ],
)

print("✅ Django configuration successful!")
print("=" * 50)
