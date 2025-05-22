from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Boards(models.Model):
    name = models.CharField(max_length=100)
    board_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.user}: {self.name}"


class Items(models.Model):
    TYPE_CHOICE = (
        ('img', 'images'),
        ('txt', 'texts'),
        ('stick', 'sticky_notes'),

    )

    board = models.ForeignKey(Boards, on_delete=models.CASCADE, related_name='items')
    x_coordinate = models.DecimalField(max_digits=10, decimal_places=2)
    y_coordinate = models.DecimalField(max_digits=10, decimal_places=2)
    item_id = models.CharField(default=0, db_index=True)
    type = models.CharField(max_length=15, choices=TYPE_CHOICE)
    content = models.JSONField()

    def __str__(self):
        return f"{self.board}: {self.type}, {self.item_id}"
