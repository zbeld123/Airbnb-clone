from django.contrib import admin
from django.utils.html import mark_safe  # html요소가 안전함을 장고에게 알리기 위함
from . import models


# 인라인 모델
# 포토모델을 룸 어드민에서 사용하기 위함
class PhotoInline(admin.TabularInline):
    model = models.Photo


# Register your models here.
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """ Room Admin Definitions """

    inlines = (PhotoInline,)  # 생성한 포토모델 인라인화

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
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

    raw_id_fields = ("host",)

    # ^: startwidth     =:exactly
    # fk관계에 접근시 . 대신 __를 사용
    search_fields = ("^city", "^host__username")

    ordering = ("price", "bedrooms")

    # fk관계 데이터 가져오기
    def count_amenities(self, obj):
        return obj.amenities.count()

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "pohoto count"


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


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):

    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        return mark_safe(f'<img src="{obj.file.url}" width=80px/>')

    get_thumbnail.short_description = "Thumbnail"
