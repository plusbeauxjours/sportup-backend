import graphene
from . import types, queries, mutations


class Query(object):
    sport_query = graphene.Field(
        types.SportQueryReponse,
        resolver=queries.resolve_sport_query,
        required=True,
        args={},
    )


class Mutation(object):

    sport_mutation = mutations.SportMutation.Field(required=True)
