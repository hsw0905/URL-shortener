from rest_framework.routers import SimpleRouter
from .views import AccountViewSet

router = SimpleRouter(trailing_slash=False)
router.register('', AccountViewSet, basename='users')
# router.register('login/', AccountViewSet, basename='login')
urlpatterns = router.urls