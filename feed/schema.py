import graphene
from . import types, queries, mutations


class Query(object):
    my_feed = graphene.Field(
        types.MyFeedResponse,
        resolver=queries.resolve_my_feed,
        required=True,
        args={},
    )


class Mutation(object):

    port_mutation = mutations.PostMutation.Field(required=True)
