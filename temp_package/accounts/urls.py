# accounts/urls.py
from django.urls import path
from .views import profile_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),  # 处理/accounts/profile/
]