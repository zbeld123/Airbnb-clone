from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

    list_display = (
        "name",
        "host",
        "country",
        "city",
        "price",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
    )

    list_filter = ("city", "instant_book", "country")

    # ^: startwidth     =:exactly
    # fk관계에 접근시 . 대신 __를 사용
    search_fields = ("^city", "^host__username")


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class RoomTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ """

    pass
