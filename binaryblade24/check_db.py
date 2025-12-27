import os
import django
import sys
from django.db import connection

# Set up Django environment
sys.path.append(os.path.abspath('.'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(User_user)")
        columns = cursor.fetchall()
        for col in columns:
            print(col[1])

if __name__ == "__main__":
    check_columns()
