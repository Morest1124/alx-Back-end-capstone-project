"""
URL configuration for binaryblade24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import api_home

urlpatterns = [
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('User.urls', namespace='user_api')),
    path('api/projects/', include('Project.urls', namespace='project_api')),
    path('api/comments/', include('Comment.urls', namespace='comment_api')),
    path('api/dashboard/', include('dashboard.urls', namespace='dashboard_api')),
    path('api/messages/', include('message.urls', namespace='message_api')),
    path('api/api-key/', include('apikey.urls', namespace='apikey_api')),
    path('api/proposals/', include('Proposal.urls', namespace='proposal_api')),
    path('api/orders/', include('Order.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)