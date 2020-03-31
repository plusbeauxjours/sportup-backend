import graphene
from . import types, queries, mutations


class Query(object):
    event_query = graphene.Field(
        types.EventQueryReponse,
        resolver=queries.resolve_event_query,
        required=True,
        args={},
    )


class Mutation(object):
    create_event = mutations.CreateEvent.Field(required=True)
    register_team = mutations.RegisterTeam.Field(required=True)
