from django.contrib import admin
from .models import Task, TaskCommentModel

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "board", "status", "priority", "assignee", "reviewer", "due_date")
    list_filter = ("status", "priority", "board")
    search_fields = ("title", "description", "assignee__username", "reviewer__username")


@admin.register(TaskCommentModel)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author", "created_at")
    search_fields = ("task__title", "author__username", "content")
