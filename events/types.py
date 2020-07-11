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


class GetEventResponse(graphene.ObjectType):
    event = graphene.Field(EventType)


class GetRegistrationsResponse(graphene.ObjectType):
    registrations = graphene.List(RegistrationType)


class GetSearchEventsResponse(graphene.ObjectType):
    events = graphene.List(EventType)


class GetUpcomingEventsResponse(graphene.ObjectType):
    events = graphene.List(EventType)


class CreateEventResponse(graphene.ObjectType):
    event = graphene.Field(EventType)


class RegisterTeamResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class ApproveRegistrationResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class DisapproveRegistrationResponse(graphene.ObjectType):
    ok = graphene.Boolean()
