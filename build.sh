#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python binaryblade24/manage.py collectstatic --no-input
python binaryblade24/manage.py migrate
python binaryblade24/manage.py createsuperuser --no-input || echo "Superuser already exists."t


#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python binaryblade24/manage.py collectstatic --no-input
python binaryblade24/manage.py migrate

# Use Python to check if a user exists and create/update if needed.


SUPERUSER_USERNAME="${DJANGO_SUPERUSER_USERNAME:-DJANGO_SUPERUSER_USERNAME}"
SUPERUSER_EMAIL="${DJANGO_SUPERUSER_EMAIL:-DJANGO_SUPERUSER_EMAIL}"
SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-DJANGO_SUPERUSER_PASSWORD}"

# The -c flag runs a command and exits. This creates or updates the user.
python binaryblade24/manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    # Try to get the existing user
    user = User.objects.get(username='$SUPERUSER_USERNAME')
    # If the user exists, only update the password/email if the env vars are set
    user.email = '$SUPERUSER_EMAIL'
    user.set_password('$SUPERUSER_PASSWORD')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print('Superuser updated successfully.')
except User.DoesNotExist:
    # If the user doesn't exist, create it
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print('Superuser created successfully.')
"