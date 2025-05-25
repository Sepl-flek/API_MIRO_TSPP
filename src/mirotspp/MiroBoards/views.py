import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from MiroBoard import MiroBoard
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
        tasks.to_update_items(self.kwargs.get('board_id'))
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
        # todo block else

        serializer.save(board=board, item_id=str(item_id))


@login_required
def board_items_list(request, board_id):
    board = get_object_or_404(Boards, id=board_id, user=request.user)
    items = Items.objects.filter(board=board)
    return render(request, 'MiroBoards/board_items.html', {'board': board, 'items': items})


class SaveItemView(View):
    def post(self, request, item_id, board_id):

        item_type = json.loads(request.body).get("type")
        board = get_object_or_404(Boards, pk=board_id)
        miro = MiroBoard(board.board_id, board.api_key)

        try:
            if item_type == "stick":
                success = miro.get_sticker(item_id)
            elif item_type == "img":
                success = miro.get_image(item_id)
            elif item_type == "txt":
                success = miro.get_text(item_id)
            else:
                return JsonResponse({"error": "Unknown item type"}, status=400)

            if success:
                return JsonResponse({"success": True})
            return JsonResponse({"error": "Failed to save"}, status=500)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
