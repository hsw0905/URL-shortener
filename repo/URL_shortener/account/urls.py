from rest_framework.routers import SimpleRouter
from .views import AccountViewSet

router = SimpleRouter(trailing_slash=False)
router.register('', AccountViewSet, basename='users')
urlpatterns = router.urls