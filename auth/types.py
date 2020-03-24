import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType


class UserType(DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = get_user_model()

    def resolve_name(self, info):
        return self.get_full_name()


class CreateUserReponse(graphene.ObjectType):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)
