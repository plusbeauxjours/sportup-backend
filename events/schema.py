import graphene
from . import types, queries, mutations


class Query(object):
    get_event = graphene.Field(
        types.GetEventResponse,
        resolver=queries.resolve_get_event,
        required=True,
        args={"event_id": graphene.String(required=True)},
    )
    get_registrations = graphene.Field(
        types.GetRegistrationsResponse,
        resolver=queries.resolve_get_registrations,
        required=True,
        args={"event_id": graphene.String(required=True)},
    )
    get_search_events = graphene.Field(
        types.GetSearchEventsResponse,
        resolver=queries.resolve_get_search_events,
        required=True,
        args={"search_text": graphene.String(required=True)},
    )
    get_upcoming_events = graphene.Field(
        types.GetUpcomingEventsResponse,
        resolver=queries.resolve_get_upcoming_events,
        required=True,
        args={},
    )


class Mutation(object):
    create_event = mutations.CreateEvent.Field(required=True)
    register_team = mutations.RegisterTeam.Field(required=True)
    approve_registration = mutations.ApproveRegistration.Field(required=True)
    disapprove_registration = mutations.DisapproveRegistration.Field(required=True)
