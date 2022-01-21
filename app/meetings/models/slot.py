from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import models

from profiles.models import UserProfile


class Slot(models.Model):
    class DurationChoices(models.IntegerChoices):
        MIN_15 = (15, '15 Min')
        MIN_30 = (30, '30 Min')
        MIN_45 = (45, '45 Min')

    user = models.ForeignKey(UserProfile, related_name="slots", on_delete=models.CASCADE)
    scheduled_at = models.DateTimeField()  # must not be at the bast - must not conflict with other slots
    duration = models.SmallIntegerField(choices=DurationChoices.choices)

    def _clean_scheduled_at(self):
        """
        Performs extra cleaning and validation on scheduled_at field.
        """
        try:
            SlotValidator.validate_scheduled_at_is_available(
                self, ValidationError
            )
        except ValidationError as e:
            raise ValidationError({"scheduled_at": e.message})

    def clean(self):
        self._clean_scheduled_at()
        return super(Slot, self).clean()

    def __str__(self):
        """
        Return string representation for model object.

        Returns:
            (str): string representation using user email, schedule time and duration.
        """
        return f"User({self.user.email}) Slot({self.scheduled_at}) Duration({self.duration})"

    def is_empty(self):
        return not bool(self.meeting)


class SlotValidator:
    """
    This will handle common validation that can not be automatically handled
    by Django nor graphene-django Framework.
    """

    @staticmethod
    def validate_scheduled_at_is_available(instance, exception):
        """
        This validates the scheduled_at of a Slot instance to be
        supported.

        :param instance: The Slot instance to validate.
        :param exception: The exception to be raised when validation is not
            successful.
        """
        present = timezone.now()
        if instance.scheduled_at < present:
            raise exception(
                "Slot time must NOT be in the PAST."
            )
        available_slots_day = Slot.objects. \
            filter(scheduled_at__gte=present.date()). \
            values('scheduled_at', 'duration')
        if instance.pk is not None:
            available_slots_day = available_slots_day.exclude(id=instance.id)
        for slot in available_slots_day:
            if slot['scheduled_at'] <= instance.scheduled_at <= slot['scheduled_at'] + timedelta(
                    minutes=slot['duration']) or \
                    instance.scheduled_at <= slot['scheduled_at'] <= instance.scheduled_at + \
                    timedelta(minutes=instance.duration):
                raise exception(
                    f"This slot conflicts with slot from "
                    f"{slot['scheduled_at']} to {slot['scheduled_at'] + timedelta(minutes=slot['duration'])}")
