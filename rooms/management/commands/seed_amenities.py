from django.core.management.base import BaseCommand
from rooms.models import Amenity


class Command(BaseCommand):

    """ Custom django-admin commands """

    help = "This commands is creates amenity elements in model"

    def handle(self, *args, **options):
        amenities = [
            "Kitchen",
            "Shampoo",
            "Heating",
            "Air conditioning",
            "Washer",
            "Dryer",
            "Wifi",
            "Breakfast",
            "Indoor fireplace",
            "Hangers",
            "Iron",
            "Hair dryer",
            "Laptop-friendly workspace",
            "TV",
            "Crib",
            "High chair",
            "Self check-in",
            "Smoke alarm",
            "Carbon monoxide alarm",
            "Private bathroom",
            "Beachfront",
            "Waterfront",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)  # Amenity의 name모델에 배열의 모든 요소 생성
        self.stdout.write(self.style.SUCCESS("Amenities created!!"))  # 정상적 실행시 출력문
