# news/urls.py
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet

router = DefaultRouter()         #จะทำทุกอย่างให้อัตโนมัติ
router.register(r'news', NewsViewSet, basename='news')   #จะเรียกใช้ในหน้า Views.py โดยอัตโนมัติ

urlpatterns = router.urls
