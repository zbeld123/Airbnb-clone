from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Conversation)
class ConversationAdmin(admin.ModelAdmin):

    """ Conversation Admin Definition """

    filter_horizontal = ("participants",)

    list_display = (
        "__str__",
        "count_particopants",
        "count_messages",
    )


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):

    """ Message Admin Definition """

    list_display = (
        "__str__",
        "created",
    )

