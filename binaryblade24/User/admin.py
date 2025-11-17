from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Role

# Register the custom User model so it is manageable via Django admin
User = get_user_model()


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email', 'first_name', 'last_name')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	ordering = ('username',)
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'roles')}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
		('Custom fields', {'fields': ('country_origin', 'phone_number', 'identity_number')}),
	)
	readonly_fields = ('last_login', 'date_joined')

	def save_model(self, request, obj, form, change):
		if not change:  # When creating a new user
			obj.is_active = True
		super().save_model(request, obj, form, change)
