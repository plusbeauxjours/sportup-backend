import graphene
from graphene_django.types import DjangoObjectType
from . import models


class EventType(DjangoObjectType):
    class Meta:
        model = models.Event


class EventQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class EventMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()
