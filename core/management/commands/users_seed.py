import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from sports import models as sport_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_seeder = Seed.seeder()
        user_seeder.add_entity(
            user_models.User,
            2,
            {
                "user_img": None,
                "push_token": None,
                "is_staff": False,
                "is_superuser": False,
                "bio": lambda x: user_seeder.faker.text(),
            },
        )
        user_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Users seeded"))

        ups_seeder = Seed.seeder()
        all_users = user_models.User.objects.all()
        all_sports = sport_models.Sport.objects.all()
        ups_seeder.add_entity(
            user_models.UserPlaysSport,
            50,
            {
                "user": lambda x: random.choice(all_users),
                "sport": lambda x: random.choice(all_sports),
            },
        )
        ups_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"UserPlaysSports seeded"))

        all_ups = user_models.UserPlaysSport.objects.all()
        urs_seeder = Seed.seeder()
        urs_seeder.add_entity(
            user_models.UserRatesSport,
            50,
            {
                "rated_user_sport": lambda x: random.choice(all_ups),
                "rating": lambda x: random.randint(0, 5),
                "rated_by": lambda x: random.choice(all_users),
            },
        )
        urs_seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"UserRatesSports seeded"))
