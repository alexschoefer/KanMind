from django.db import models
from django.contrib.auth.models import User


class Board(models.Model):
    """
    Represents a project board that groups users and tasks.

    A board has exactly one owner and can have multiple members.
    The owner is always implicitly considered a member of the board.
    """

    title = models.CharField(
        max_length=255,
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards",
    )

    members = models.ManyToManyField(
        User,
        related_name="boards",
    )

    def __str__(self):
        """
        Return representation of the board.

        Returns:
            str: The board title.
        """
        return self.title
