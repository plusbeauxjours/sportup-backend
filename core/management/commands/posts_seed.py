import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from feed import models as feed_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_users = user_models.User.objects.all()
        post_seeder = Seed.seeder()
        post_seeder.add_entity(
            feed_models.Post,
            1000,
            {
                "posted_by": lambda x: random.choice(all_users),
                "text": lambda x: post_seeder.faker.text(),
                "post_img": False,
                "score": lambda x: random.randint(-5, 20),
            },
        )
        post_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Posts seeded"))
