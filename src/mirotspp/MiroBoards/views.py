from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from MiroBoards.models import Boards, Items
from MiroBoards.serializers import BoardsSerializer, ItemSerializer


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
        board = Boards.objects.get(
            id=self.kwargs.get('board_id'),
            user=self.request.user
        )
        serializer.save(board=board)

@login_required
def board_items_list(request, board_id):
    board = get_object_or_404(Boards, id=board_id, user=request.user)
    items = Items.objects.filter(board=board)
    return render(request, 'MiroBoards/board_items.html', {'board': board, 'items': items})