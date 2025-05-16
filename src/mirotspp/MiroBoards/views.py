from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from MiroBoards.models import Boards
from MiroBoards.serializers import BoardsSerializer


# Create your views here.
class BoardsViewSet(ModelViewSet):
    serializer_class = BoardsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Boards.objects.filter(user=self.request.user).prefetch_related('items')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)