from rest_framework.routers import DefaultRouter

from Auth.views import AuthViewSet, TodoViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, base_name='auth')
router.register(r'todo', TodoViewSet, base_name='todo')