import random
from datetime import datetime, timedelta

# timedelta : 날짜간 사칙연산 가능토록 ?
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservations_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command is create reservation seeds"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", type=int, default=1, help="How many want to create reservations"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_rooms = room_models.Room.objects.all()
        seeder.add_entity(
            reservations_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(all_users),
                "room": lambda x: random.choice(all_rooms),
                # 체크아웃 날짜가 체크인 시간보다 난수만큼 뒤에 있도록
                "check_in": lambda x: datetime.now(),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(3, 25)),
            },
        )
        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} create reservations !!!"))
