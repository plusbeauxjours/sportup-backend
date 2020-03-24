import graphene
from . import types, queries, mutations


class Query(object):
    port_query = graphene.Field(
        types.PostQueryReponse,
        resolver=queries.resolve_post_query,
        required=True,
        args={},
    )


class Mutation(object):

    port_mutation = mutations.PostMutation.Field(required=True)
