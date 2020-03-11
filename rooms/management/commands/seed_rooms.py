import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models


class Command(BaseCommand):

    help = "This command is creates Room"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many rooms you want to create"
        )

    def handle(self, *args, **options):
        room_number = options.get("number")
        # seed를 통해 더미데이터를 생성할 때 fk관계에 있는 데이터는 가져오지 못함.
        # FK관계의 데이터를 가져오기 위해 모든 데이터를 가져오지만 실제로 데이터베이스의 모든 데이터를 (all())가져오는 것은 바람직하지 않음.
        # FK관계의 모든 데이터를 가져오고 난수를 통해 랜덤한 데이터를 가져올 수 있음.
        all_user = user_models.User.objects.all()
        all_roomtype = room_models.RoomType.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            room_models.Room,
            room_number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_user),
                "room_type": lambda x: random.choice(all_roomtype),
                "price": lambda x: random.randint(100, 500),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )
        created_photos = seeder.execute()  # seeder의 PK값 리턴?
        created_clean = flatten(list(created_photos.values()))  # dict에 이중리스트 구조이므로 변환
        all_amenities = room_models.Amenity.objects.all()
        all_facilities = room_models.Facility.objects.all()
        all_houserules = room_models.HouseRule.objects.all()
        for pk in created_clean:
            room = room_models.Room.objects.get(pk=pk)
            for i in range(3, random.randint(10, 30)):  # Room당 사진 갯수 (3장 이상 10~17장 이하)
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,
                    file=f"room_photos/{random.randint(1, 31)}.webp",
                )
            # Many-to-Many관계 더미더이터 추가
            for a in all_amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in all_facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in all_houserules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.houserules.add(r)

        self.stdout.write(self.style.SUCCESS(f"{room_number} rooms created !!!"))

