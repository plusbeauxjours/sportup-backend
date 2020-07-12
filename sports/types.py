import graphene
from graphene_django.types import DjangoObjectType
from . import models


class SportType(DjangoObjectType):
    sport_id = graphene.String()

    class Meta:
        model = models.Sport

    def resolve_sport_id(self, info):
        return self.id


class GetAllSportReponse(graphene.ObjectType):
    sports = graphene.List(SportType)
