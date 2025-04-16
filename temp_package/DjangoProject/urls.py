# DjangoProject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import api_root

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/accounts/', include('accounts.api_urls')),  # API路由 → 指向新文件
    path('accounts/', include('accounts.urls')),          # 非API路由 → 新增
    path('api/finance/', include('finance.urls')),
    path('api/reporting/', include('reporting.urls')),
    path('api/audit/', include('audit.urls')),
    path('api/system/', include('system.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='index.html')),
]