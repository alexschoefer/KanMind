from django.db import models
from django.contrib.auth.models import User
from board_app.models import Board


class Task(models.Model):
    """
    Represents a task within a board.

    A task belongs to exactly one board and can optionally be assigned
    to a user and reviewed by another user. Tasks can have different
    statuses and priorities to reflect their workflow state.
    """

    board = models.ForeignKey(Board,related_name="tasks",on_delete=models.CASCADE,)

    title = models.CharField(max_length=255,)

    description = models.TextField(blank=True,)

    status = models.CharField(max_length=20,
        choices=[
            ("to-do", "To Do"),
            ("in-progress", "In Progress"),
            ("review", "Review"),
            ("done", "Done"),
        ],
    )

    priority = models.CharField(
        max_length=10,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
    )

    assignee = models.ForeignKey(User,related_name="assigned_tasks",null=True,blank=True,on_delete=models.SET_NULL,)

    reviewer = models.ForeignKey(User,related_name="review_tasks",null=True,blank=True,on_delete=models.SET_NULL,)

    due_date = models.DateField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,)

    updated_at = models.DateTimeField(auto_now=True,)

    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_tasks",null=True,blank=True,)

    def __str__(self):
        """
        Return a human-readable representation of the task.

        Returns:
            str: The task title and associated board title.
        """
        return f"{self.title} ({self.board.title})"


class TaskCommentModel(models.Model):
    """
    Represents a comment made on a task.

    Each comment is authored by a user and belongs to a specific task.
    """

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True,)

    author = models.ForeignKey(User,on_delete=models.CASCADE,elated_name="task_comments",)

    content = models.TextField(max_length=255,null=True,blank=True)

    task = models.ForeignKey(Task,on_delete=models.CASCADE, related_name="comments",null=True,blank=True,)

    def __str__(self):
        """
        Return representation of the comment.

        Returns:
            str: Author and task reference.
        """
        return f"Comment by {self.author} on task {self.task_id}"
