import graphene
from graphene_django.types import DjangoObjectType
from . import models


class TeamType(DjangoObjectType):
    class Meta:
        model = models.Team


class TeamQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class TeamMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()
