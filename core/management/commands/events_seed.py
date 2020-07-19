import random
import datetime
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from events import models as event_models
from sports import models as sport_models


class Command(BaseCommand):
    def random_dates(start, end, n, seed=1, replace=False):
        dates = pd.date_range(start, end).to_series()
        return dates.sample(n, replace=replace, random_state=seed)

    def handle(self, *args, **options):
        all_users = user_models.User.objects.all()
        all_sports = sport_models.Sport.objects.all()

        event_seeder = Seed.seeder()
        event_seeder.add_entity(
            event_models.Event,
            500,
            {
                "name": lambda x: event_seeder.faker.word(),
                "description": lambda x: event_seeder.faker.text(),
                "cover_img": None,
                "document": None,
                "sport": lambda x: random.choice(all_sports),
                "start_date": lambda x: event_seeder.faker.future_date(end_date="+60d"),
                "end_date": lambda x: event_seeder.faker.future_date(end_date="+240d"),
                "start_time": lambda x: event_seeder.faker.time(),
                "end_time": lambda x: event_seeder.faker.time(),
                "minimum_members": lambda x: random.randint(1, 5),
                "maximum_members": lambda x: random.randint(5, 10),
                "expected_teams": lambda x: random.randint(-5, 20),
                "owner": lambda x: random.choice(all_users),
                "latitude": lambda x: random.uniform(-90, 90),
                "longitude": lambda x: random.uniform(-180, 180),
            },
        )
        event_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Events seeded"))

