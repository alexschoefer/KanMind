from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner")
    search_fields = ("title", "owner__username", "owner__email")
    filter_horizontal = ("members",) 

admin.site.register(Board, BoardAdmin)