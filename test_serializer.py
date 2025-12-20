import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'binaryblade24.settings')
django.setup()

try:
    from Project.Serializers import ProjectSerializer
    from Project.models import Project
    
    print("Attempting to initialize ProjectSerializer...")
    # Get a dummy project or just try to access fields
    serializer = ProjectSerializer()
    fields = serializer.fields
    print(f"Successfully loaded fields: {list(fields.keys())}")
    
    if 'view_count' in fields:
        print("SUCCESS: view_count is present in fields.")
    else:
        print("FAIL: view_count is NOT present in fields.")
        
    if 'debug_sync_field' in fields:
        print("SUCCESS: debug_sync_field is present in fields.")
    else:
        print("FAIL: debug_sync_field is NOT present in fields.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
