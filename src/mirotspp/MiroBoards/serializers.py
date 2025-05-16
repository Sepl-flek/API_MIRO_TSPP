from rest_framework.serializers import ModelSerializer

from MiroBoards.models import Boards, Items


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Items
        fields = ('board', 'x_coordinate', 'y_coordinate', 'item_id', 'type', 'content')


class BoardsSerializer(ModelSerializer):
    class Meta:
        model = Boards
        fields = ('id', 'name', 'board_id', 'api_key')
