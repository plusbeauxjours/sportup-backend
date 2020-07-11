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
        return user.is_team_admin(team=self)


class GetTeamResponse(graphene.ObjectType):
    team = graphene.Field(TeamType)


class GetTeamsForGameResponse(graphene.ObjectType):
    teams = graphene.List(TeamType)


class GetTeamsForPlayerResponse(graphene.ObjectType):
    teams = graphene.List(TeamType)


class GetSearchTeamsResponse(graphene.ObjectType):
    teams = graphene.List(TeamType)


class CreateTeamResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class AddTeamMemberResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RemoveTeamMemberResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class UpdateTeamResponse(graphene.ObjectType):
    team = graphene.Field(TeamType)


class RatesTeamResponse(graphene.ObjectType):
    ok = graphene.Boolean()
