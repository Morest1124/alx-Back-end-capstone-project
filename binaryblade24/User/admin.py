from django.contrib import admin
from django.contrib.auth import get_user_model

# Register the custom User model so it is manageable via Django admin
User = get_user_model()


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	ordering = ('username',)
