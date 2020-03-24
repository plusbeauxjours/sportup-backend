import graphene
from graphene_django.types import DjangoObjectType
from . import models


class SportType(DjangoObjectType):
    class Meta:
        model = models.Sport


class SportQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class SportMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()
