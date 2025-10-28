from django.contrib import admin
from rest_framework_api_key.models import APIKey


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "created", "expiry_date", "revoked", "hashed_key")
    list_filter = ("created", "revoked")
    search_fields = ("name",)
