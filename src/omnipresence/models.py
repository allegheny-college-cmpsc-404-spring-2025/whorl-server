import pgtrigger
from datetime import datetime
from django.db import models


class OmnipresenceModel(models.Model):
    """
    Omnipresence Tracking Model

    Represents an omnipresence tracking system for users, storing information
    about usernames, character names, working directories, last active timestamps,
    and active status.

    Fields:
        - username (str): The username of the user.
        - charname (str): The unique character name associated with the user.
        - working_dir (str): The working directory of the user.
        - last_active (datetime): The timestamp of the user's last activity.
        - is_active (bool): Indicates whether the user is currently active.

    Methods:
        - as_dict(): Converts the model instance into a dictionary representation.
    """

    username = models.CharField(max_length = 255)
    charname = models.CharField(max_length = 255, unique = True)
    working_dir = models.CharField(max_length = 512)
    last_active = models.DateTimeField(auto_now = True)
    is_active = models.BooleanField(default = True)

    def as_dict(self):
        """
        Convert the model instance into a dictionary representation.

        Returns:
            dict: A dictionary containing the field names and their values.
        """
        result = {}
        fields = self._meta.fields
        for field in fields:
            result[field.name] = getattr(self, field.name)
        return result
