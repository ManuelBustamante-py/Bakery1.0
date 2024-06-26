# baker_1_0_0/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),  # Incluir las URLs de la aplicación frontend
]
