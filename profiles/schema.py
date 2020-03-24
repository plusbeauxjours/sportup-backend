import graphene
from . import types, queries, mutations


class Query(object):
    profile_query = graphene.Field(
        types.ProfileQueryReponse,
        resolver=queries.resolve_profile_query,
        required=True,
        args={},
    )


class Mutation(object):

    profile_mutation = mutations.ProfileMutation.Field(required=True)
