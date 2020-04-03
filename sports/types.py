import graphene
from graphene_django.types import DjangoObjectType
from . import models


class SportType(DjangoObjectType):
    sport_uuid = graphene.String()

    class Meta:
        model = models.Sport

    def resolve_sport_uuid(self, info):
        return self.uuid


class GetAllSportReponse(graphene.ObjectType):
    sports = graphene.List(SportType)
