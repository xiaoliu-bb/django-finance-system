# audit/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.AuditLogViewSet, basename='audit-log')  # 注册ViewSet

urlpatterns = [
    path('login-history/', views.UserLoginHistoryView.as_view(), name='login-history'),
    path('model-changes/<str:model_name>/', views.ModelChangeListView.as_view(), name='model-changes'),
] + router.urls