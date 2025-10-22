from django.db import migrations

def populate_roles(apps, schema_editor):
    Role = apps.get_model('User', 'Role')
    roles = ['ADMIN', 'CLIENT', 'FREELANCER']
    for role_name in roles:
        Role.objects.create(name=role_name)

class Migration(migrations.Migration):

    dependencies = [
        ('User', '0010_role_remove_profile_role_user_roles'),
    ]

    operations = [
        migrations.RunPython(populate_roles),
    ]