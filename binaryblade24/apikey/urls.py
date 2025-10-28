from django.urls import path
from .views import GenerateAPIKeyView

app_name = 'apikey'

urlpatterns = [
    path('generate-key/', GenerateAPIKeyView.as_view(), name='generate-api-key'),
]
