import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

    def resolve_name(self, info):
        return self.get_full_name()


class MeReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class GetUserReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class CreateUserReponse(graphene.ObjectType):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)


class FollowUserResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class UnfollowUserResponse(graphene.ObjectType):
    ok = graphene.Boolean()
