import uuid
import json
import requests
import random
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User
from sports.models import Sport

sports_list = [
    "Archery",
    "Badminton",
    "Baseball",
    "Basketball",
    "BMX",
    "Bocce",
    "Bowling",
    "Boxing",
    "Broomball",
    "Cheerleading",
    "Cricket",
    "Croquet",
    "Running",
    "Curling",
    "Cycling",
    "Dance",
    "Darts",
    "Diving",
    "Dodgeball",
    "Equine Sports",
    "Fencing",
    "Field Hockey",
    "Figure Skating",
    "Fishing",
    "Floor Hockey",
    "Foosball",
    "Football",
    "Golf",
    "Gymnastics",
    "Handball",
    "Hang Gliding",
    "Horseshoes",
    "Ice Hockey",
    "Kayaking ",
    "Kickball",
    "Lacrosse",
    "Martial Arts",
    "Mountain Biking",
    "Netball",
    "Pickleball",
    "Polo",
    "Pool",
    "Powerlifting",
    "Racquetball",
    "Rock Climbing",
    "Rounders",
    "Rowing",
    "Rugby",
    "Sailing",
    "Shooting",
    "Skateboarding",
    "Skiing",
    "Skydiving",
    "Snowboarding",
    "Soccer",
    "Softball",
    "Squash",
    "Surfing",
    "Swimming",
    "Table Tennis",
    "T-Ball",
    "Team Handball",
    "Tennis",
    "Tetherball",
    "Track ",
    "Ultimate Frisbee",
    "Volleyball",
    "Wake Boarding",
    "Wallyball",
    "Water Polo",
    "Water Skiing",
    "White Water Rafting",
    "Wrestling",
    "Yoga",
]


class get_photos(object):
    def __init__(self, **kwargs):
        self.base_url = "https://api.unsplash.com/search/photos"
        self.headers = {
            "Accept-Version": "v1",
            "Authorization": "Client-ID " + settings.UNSPLASH_KEY,
        }
        self.urls = []

        self.term = kwargs.get("term")

    def get_urls(self):
        payload = {"page": "1", "query": self.term}
        req = requests.get(url=self.base_url, headers=self.headers, params=payload)
        data = json.loads(req.text)
        return data["results"][0]["urls"]["raw"]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for sport in sports_list:
            if sport.sport_img_url == None:
                try:
                    gp = get_photos(term=sport).get_urls()
                    sport_img_url = (
                        gp
                        + "?ixlib=rb-0.3.5&q=100&fm=jpg&crop=entropy&cs=faces&h=450&w=450&fit=crop"
                    )
                except:
                    sport_img_url = None

                sport = Sport.objects.create(name=sport, sport_img_url=sport_img_url)

        # rooms = Room.objects.all()
        # rooms.delete()
        # user_seeder = Seed.seeder()
        # user_seeder.add_entity(
        #     User,
        #     20,
        #     {
        #         "uuid": lambda x: uuid.uuid4(),
        #         "avatar": None,
        #         "is_staff": False,
        #         "is_superuser": False,
        #     },
        # )
        # user_seeder.execute()

        # users = User.objects.all()
        # room_seeder = Seed.seeder()
        # room_seeder.add_entity(
        #     Room,
        #     50,
        #     {
        #         "uuid": lambda x: uuid.uuid4(),
        #         "user": lambda x: random.choice(users),
        #         "name": lambda x: room_seeder.faker.street_address(),
        #         "lat": lambda x: random.uniform(40.706943, 40.822943),
        #         "lng": lambda x: random.uniform(-73.923917, -74.040000),
        #         "price": lambda x: random.randint(60, 300),
        #         "beds": lambda x: random.randint(0, 8),
        #         "bedrooms": lambda x: random.randint(0, 5),
        #         "bathrooms": lambda x: random.randint(0, 5),
        #         "instant_book": lambda x: random.choice([True, False]),
        #         "check_in": lambda x: datetime.now(),
        #         "check_out": lambda x: datetime.now(),
        #     },
        # )
        # room_seeder.execute()

        # review_seeder = Seed.seeder()
        # users = User.objects.all()
        # rooms = Room.objects.all()
        # review_seeder.add_entity(
        #     Review,
        #     1000,
        #     {
        #         "uuid": lambda x: uuid.uuid4(),
        #         "user": lambda x: random.choice(users),
        #         "text": lambda x: review_seeder.faker.text(),
        #         "room": lambda x: random.choice(rooms),
        #     },
        # )
        # review_seeder.execute()

        # rooms = Room.objects.all()
        # for room in rooms:
        #     for i in range(random.randint(3, 6)):
        #         Photo.objects.create(
        #             caption=room_seeder.faker.sentence(),
        #             room=room,
        #             file=f"room_photos/{random.randint(1, 50)}.jpeg",
        #         )
        self.stdout.write(self.style.SUCCESS(f"Everything seeded"))
