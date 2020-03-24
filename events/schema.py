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

    event_mutation = mutations.EventMutation.Field(required=True)
