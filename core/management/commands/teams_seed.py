import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from users import models as user_models
from teams import models as team_models
from sports import models as sport_models


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_sports = sport_models.Sport.objects.all()
        all_users = user_models.User.objects.all()
        team_seeder = Seed.seeder()
        team_seeder.add_entity(
            team_models.Team,
            100,
            {
                "team_name": lambda x: team_seeder.faker.word(),
                "cover_img": None,
                "sport": lambda x: random.choice(all_sports),
                "created_by": lambda x: random.choice(all_users),
            },
        )
        team_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"Teams seeded"))

        all_teams = team_models.Team.objects.all()
        all_users = user_models.User.objects.all()
        tm_seeder = Seed.seeder()
        tm_seeder.add_entity(
            team_models.TeamMember,
            500,
            {
                "team": lambda x: random.choice(all_teams),
                "user": lambda x: random.choice(all_users),
                "is_admin": False,
            },
        )
        tm_seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"TeamMember seeded"))

        all_teams = team_models.Team.objects.all()
        all_users = user_models.User.objects.all()
        urt_seeder = Seed.seeder()
        urt_seeder.add_entity(
            team_models.UserRatesTeam,
            1000,
            {
                "team": lambda x: random.choice(all_teams),
                "rating": lambda x: random.randint(0, 5),
                "rated_by": lambda x: random.choice(all_users),
            },
        )
        urt_seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"UserRatesTeam seeded"))
