import graphene
from graphene_django.types import DjangoObjectType
from . import models


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post


class PostQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class PostMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()
