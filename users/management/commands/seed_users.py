from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        user_number = options.get("number")
        seeder = Seed.seeder()
        seeder.add_entity(
            User, user_number, {"is_staff": False, "is_superuser": False,}
        )
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{user_number} users created !!"))

