from django.db import models

from .slot import Slot


class Meeting(models.Model):
    slot = models.OneToOneField(Slot, related_name="meeting", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    attendance_full_name = models.CharField(max_length=255)
    attendance_email_address = models.EmailField(max_length=255)

    def __str__(self):
        """
        Return string representation for model object.

        Returns:
            (str): string representation using name attendance name and email - and slot duration.
        """
        return f"Meeting({self.name}) with({self.attendance_full_name} - {self.attendance_email_address}) " \
               f"Duration({self.slot.duration})"
