import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from . import models


class EventType(DjangoObjectType):
    is_owner = graphene.Boolean()

    class Meta:
        model = models.Event

    @login_required
    def resolve_is_owner(self, info):
        user = info.context.user
        return user.pk == self.owner.pk


class RegistrationType(DjangoObjectType):
    class Meta:
        model = models.Registration


class RegisteredPlayerType(DjangoObjectType):
    class Meta:
        model = models.RegisteredPlayer


class EventQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class CreateEventReponse(graphene.ObjectType):
    event = graphene.Field(EventType)


class RegisterTeamResponse(graphene.ObjectType):
    ok = graphene.Boolean()
