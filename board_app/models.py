from django.db import models
from django.contrib.auth.models import User

class Board(models.Model):
    title=models.CharField(max_length=255)
    #Ein Board gehört genau zu EINEM user, ein User kann aber mehrere Boards besitzen => 1:n Beziehung!
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_boards"
    )
    members = models.ManyToManyField(
        User,
        related_name="boards"
    )

    def __str__(self):
        return self.title

