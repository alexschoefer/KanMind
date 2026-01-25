from django.db import models
from board_app.models import Board

class Task(models.Model):
    board = models.ForeignKey(
        Board,
        related_name="tasks",
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('to-do','To Do'),('in-progress','In Progress'), ('review', 'Review'), ('done','Done')])
    priority = models.CharField(max_length=10, choices=[('low','Low'),('medium','Medium'),('high','High')], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.board.title})"
