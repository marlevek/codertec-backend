from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),  # 🔹 Inclui as rotas do app chatbot
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)