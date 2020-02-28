from django.db import models
from core import models as core_models

# Create your models here.


class Review(core_models.TimeStampedModel):
    """ Review Model Definition """

    review = models.TextField()
    check_in = models.IntegerField()
    communication = models.IntegerField()
    accuracy = models.IntegerField()
    location = models.IntegerField()
    cleanliness = models.IntegerField()
    value = models.IntegerField()

    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.review} - {self.room.name}"

