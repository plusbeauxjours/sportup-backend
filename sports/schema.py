import graphene
from . import types, queries


class Query(object):
    get_all_sports = graphene.Field(
        types.GetAllSportReponse,
        resolver=queries.resolve_get_all_sports,
        required=True,
        args={},
    )


class Mutation(object):
    pass
