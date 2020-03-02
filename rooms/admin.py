from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")},),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")},),
        (
            "More About Spaces",
            {
                "classes": ("collapse",),  # show and hide!!
                "fields": ("amenities", "facilities", "houserules"),
            },
        ),
        ("Last Details", {"fields": ("host",)},),
    )

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
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    list_filter = (
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "houserules",
        "city",
        "country",
    )

    # Many-to-Many 필터링
    filter_horizontal = (
        "amenities",
        "facilities",
        "houserules",
    )

    # ^: startwidth     =:exactly
    # fk관계에 접근시 . 대신 __를 사용
    search_fields = ("^city", "^host__username")

    ordering = ("price", "bedrooms")

    # fk관계 데이터 가져오기
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class RoomItemAdmin(admin.ModelAdmin):

    """ RoomItem Admin Definition """

    list_display = (
        "name",
        "count_items",
    )

    # many-to-many 관계 데이터 가져오기
    def count_items(self, obj):
        return obj.rooms.count()

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ """

    pass
