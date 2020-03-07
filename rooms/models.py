from django.db import models
from core import models as core_models
from users import models as user_models
from django_countries.fields import CountryField


# Create your models here.


class AbstractItem(core_models.TimeStampedModel):
    """ AbstractItem Definitions """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """RoomType Object Definition"""

    pass

    class Meta:
        verbose_name = "Room Type"


class Amenity(AbstractItem):

    """Amenity Object Definition"""

    pass

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """Facility Object Definition"""

    pass

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """HouseRule Object Definition"""

    pass

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """Photo Models Definitions"""

    caption = models.CharField(max_length=80)
    file = models.ImageField(upload_to="room_photos", blank=True)
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):
    """ Rooms Model Definitions """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    price = models.IntegerField()
    address = models.CharField(max_length=140)
    guests = models.IntegerField(default=0)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )
    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    houserules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    def __str__(self):
        return self.name

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        for review in all_reviews:
            all_ratings += review.rating_average()
        if len(all_reviews):
            return round(all_ratings / len(all_reviews))
        return 0

    # save메서드 오버라이딩
    # 저장되는 순간에 수행하고 싶은 작업을 한 후에 super().save(...)로 저장하도록.
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)  # 첫번째 문자를 대문자로 변환하도록.
        # ex) self.city = "Test" --> 어떤 내용으로 수정해서 저장하든 "Test"로 변경 후에 저장되기 때문에 Test가 저장됨.
        super().save(*args, **kwargs)
