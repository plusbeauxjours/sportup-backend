import graphene
from . import types, queries


class Query(object):
    all_sports = graphene.Field(
        types.AllSportReponse,
        resolver=queries.resolve_all_sports,
        required=True,
        args={},
    )


class Mutation(object):
    pass
