from django.db import models
from core import models as core_models

# Create your models here.


class Conversation(core_models.TimeStampedModel):

    """Conversation Model Definiotion"""

    participants = models.ManyToManyField(
        "users.User", related_name="conversation", blank=True
    )

    def __str__(self):
        all_usernames = self.participants.all()  # User의 모든 데이터 가져옴
        names = []
        for name in all_usernames:
            names.append(name.username)
        return ", ".join(names)

    def count_particopants(self):
        return self.participants.count()

    def count_messages(self):
        return self.messages.count()

    count_particopants.short_description = "Number of Participants"
    count_messages.short_description = "Number of Messages"


class Message(core_models.TimeStampedModel):

    """Message Model Definiion"""

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"

