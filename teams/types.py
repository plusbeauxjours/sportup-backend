import graphene
from graphql_jwt.decorators import login_required
from graphene_django.types import DjangoObjectType
from . import models
from users import types as user_types


class TeamType(DjangoObjectType):
    is_admin = graphene.Boolean()

    class Meta:
        model = models.Team

    @login_required
    def resolve_is_admin(self, info):
        user = info.context.user
        return user.profile.is_team_admin(team=self)


class TeamQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class CreateTeamResponse(graphene.ObjectType):
    user = graphene.Field(user_types.UserType)


class AddTeamMemberResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RemoveTeamResponse(graphene.ObjectType):
    ok = graphene.Boolean()
