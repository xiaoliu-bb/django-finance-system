# system/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'settings', views.SystemSettingViewSet, basename='system-setting')
router.register(r'fiscal-years', views.FiscalYearViewSet, basename='fiscal-year')

urlpatterns = [
    path('current-fiscal-year/', views.CurrentFiscalYearView.as_view(), name='current-fiscal-year'),
    path('settings-by-type/<str:setting_type>/', views.SettingsByTypeView.as_view(), name='settings-by-type'),
] + router.urls