import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from MiroBoards.models import Boards, Items
from MiroBoards.serializers import BoardsSerializer, ItemSerializer
from . import tasks


# Create your views here.
class BoardsViewSet(ModelViewSet):
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Boards.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemsViewSet(ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Items.objects.filter(
            board__user=self.request.user,
            board_id=self.kwargs.get('board_id')
        )

    def perform_create(self, serializer):
        x = self.request.data.get('x_coordinate')
        y = self.request.data.get('y_coordinate')
        item_type = self.request.data.get('type')
        json_content = json.loads(self.request.data.get('content'))

        board = Boards.objects.get(
            id=self.kwargs.get('board_id'),
            user=self.request.user
        )

        item_id = 0
        if item_type == 'stick':
            item_id = tasks.add_sticker_to_miro(board.id, json_content, x=x, y=y)
        elif item_type == 'txt':
            item_id = tasks.add_text_to_miro(board.id, json_content, x=x, y=y)
        elif item_type == 'img':
            item_id = tasks.add_image_to_miro(board.id, json_content, x=x, y=y)
        #todo block else


        serializer.save(board=board, item_id=str(item_id))


@login_required
def board_items_list(request, board_id):
    board = get_object_or_404(Boards, id=board_id, user=request.user)
    items = Items.objects.filter(board=board)
    return render(request, 'MiroBoards/board_items.html', {'board': board, 'items': items})
