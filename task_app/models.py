from django.db import models
from django.contrib.auth.models import User
from board_app.models import Board

class Task(models.Model):
    board = models.ForeignKey(
        Board,
        related_name="tasks",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('to-do', 'To Do'),
            ('in-progress', 'In Progress'),
            ('review', 'Review'),
            ('done', 'Done'),
        ]
    )

    priority = models.CharField(
        max_length=10,
        choices=[('low', 'Low'),('medium', 'Medium'),('high', 'High')],
        default='medium'
    )

    assignee = models.ForeignKey(User,related_name="assigned_tasks",null=True,blank=True,on_delete=models.SET_NULL)
    reviewer = models.ForeignKey(User,related_name="review_tasks",null=True,blank=True,on_delete=models.SET_NULL)

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.title} ({self.board.title})"
