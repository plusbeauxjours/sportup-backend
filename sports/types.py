import graphene
from graphene_django.types import DjangoObjectType
from . import models


class SportType(DjangoObjectType):
    class Meta:
        model = models.Sport


class GetAllSportReponse(graphene.ObjectType):
    sports = graphene.List(SportType)
