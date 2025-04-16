# accounts/api_urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet  # 假设存在API视图

router = DefaultRouter()
router.register(r'users', UserViewSet)  # 示例API端点

urlpatterns = router.urls