from django.urls import path, include
from rest_framework.routers import SimpleRouter

from MiroBoards.views import BoardsViewSet, ItemsViewSet, board_items_list, SaveItemView

router = SimpleRouter()
router.register(r'api/board', BoardsViewSet, basename='boards')
router.register(r'api/board/(?P<board_id>\d+)/items', ItemsViewSet, basename='board-items')

urlpatterns = [
    path(r'board/<int:board_id>/items/', board_items_list, name='board-item-list'),
    path('api/board/<str:board_id>/item/<str:item_id>/save/', SaveItemView.as_view(), name='save_item'),
]

urlpatterns += router.urls
