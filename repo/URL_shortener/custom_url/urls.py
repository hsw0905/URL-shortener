from rest_framework.routers import SimpleRouter
from .views import URLViewSet

router = SimpleRouter(trailing_slash=False)
router.register('', URLViewSet, basename='url_list')
urlpatterns = router.urls