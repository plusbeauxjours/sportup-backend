import graphene
from graphene_django.types import DjangoObjectType
from . import models


class ProfileType(DjangoObjectType):
    class Meta:
        model = models.Profile


class ProfileQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class ProfileMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()
