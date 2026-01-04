
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

from Project.models import Category

print("--- Checking Categories ---")
root_cats = Category.objects.filter(parent=None)
print(f"Root Categories Count: {root_cats.count()}")
for cat in root_cats:
    print(f"- {cat.name} (ID: {cat.id})")
    subcats = cat.subcategories.all()
    print(f"  Subcategories: {subcats.count()}")

all_cats = Category.objects.all()
print(f"Total Categories: {all_cats.count()}")
