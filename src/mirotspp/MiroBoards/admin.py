from django.contrib import admin
from django.contrib.admin import ModelAdmin

from MiroBoards.models import Items, Boards


# Register your models here.
@admin.register(Items)
class ItemsAdmin(ModelAdmin):
    pass


@admin.register(Boards)
class BoardsAdmin(ModelAdmin):
    pass
