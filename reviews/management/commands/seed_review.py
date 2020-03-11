import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models


class Command(BaseCommand):

    help = "This command is added review elements"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many reviews you want create"
        )

    def handle(self, *args, **options):
        review_number = options.get("number")
        all_user = user_models.User.objects.all()
        all_room = room_models.Room.objects.all()
        seeder = Seed.seeder()
        seeder.add_entity(
            review_models.Review,
            review_number,
            {
                "check_in": lambda x: random.randint(0, 5),
                "communication": lambda x: random.randint(0, 5),
                "accuracy": lambda x: random.randint(0, 5),
                "location": lambda x: random.randint(0, 5),
                "cleanliness": lambda x: random.randint(0, 5),
                "value": lambda x: random.randint(0, 5),
                "user": lambda x: random.choice(all_user),
                "room": lambda x: random.choice(all_room),
            },
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{review_number} reviews creeated !!!"))

