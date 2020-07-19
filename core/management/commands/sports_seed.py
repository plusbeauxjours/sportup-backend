import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from sports import models as sport_models

sports_list = [
    "Archery",
    "Badminton",
    "Baseball",
    "Basketball",
    "Bocce",
    "Bowling",
    "Boxing",
    "Broomball",
    "Croquet",
    "Running",
    "Cycling",
    "Darts",
    "Dodgeball",
    "Equine Sports",
    "Fencing",
    "Field Hockey",
    "Fishing",
    "Floor Hockey",
    "Foosball",
    "Football",
    "Golf",
    "Handball",
    "Kickball",
    "Lacrosse",
    "Netball",
    "Pickleball",
    "Polo",
    "Pool",
    "Racquetball",
    "Rock Climbing",
    "Rugby",
    "Shooting",
    "Skateboarding",
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
    "Ultimate Frisbee",
    "Volleyball",
    "Wallyball",
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
            print(sport)
            try:
                gp = get_photos(term=sport).get_urls()
                sport_img_url = (
                    gp
                    + "?ixlib=rb-0.3.5&q=100&fm=jpg&crop=entropy&cs=faces&h=450&w=450&fit=crop"
                )
            except:
                sport_img_url = None

            sport = sport_models.Sport.objects.create(
                name=sport, sport_img_url=sport_img_url
            )

        all_sports = sport_models.Sport.objects.all()
        for sport in all_sports:
            if sport.sport_img_url == None:
                try:
                    gp = get_photos(term=sport).get_urls()
                    sport_img_url = (
                        gp
                        + "?ixlib=rb-0.3.5&q=100&fm=jpg&crop=entropy&cs=faces&h=450&w=450&fit=crop"
                    )
                except:
                    sport_img_url = None

                sport.sport_img_url = sport_img_url
                sport.save()

        self.stdout.write(self.style.SUCCESS(f"Everything seeded"))
