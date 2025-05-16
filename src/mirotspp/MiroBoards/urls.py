from django.urls import path, include
from rest_framework.routers import SimpleRouter

from MiroBoards.views import BoardsViewSet

router = SimpleRouter()
router.register(r'api/board', BoardsViewSet, basename='boards')

urlpatterns = []

urlpatterns += router.urls
