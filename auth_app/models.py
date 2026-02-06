from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extends the built-in Django User model with additional profile information.

    Each UserProfile is linked to exactly one User instance via a one-to-one
    relationship. This model stores user-specific data that does not belong
    in the authentication model itself.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="userprofile",
    )

    fullname = models.CharField(
        max_length=80,
    )

    def __str__(self):
        """
        Return a string of the user profile.

        Returns:
            str: The full name of the user.
        """
        return self.fullname
