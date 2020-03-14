from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="frontend"),
    path('perfil/', views.profile, name="profile")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)