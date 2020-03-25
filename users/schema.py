import graphene
from . import types, queries, mutations


class Query(object):
    get_user = graphene.Field(
        types.GetUserReponse, resolver=queries.resolve_get_user, required=True, args={},
    )


class Mutation(object):

    create_user = mutations.CreateUser.Field(required=True)
    follow_user = mutations.FollowUser.Field(required=True)
    unfollow_user = mutations.UnfollowUser.Field(required=True)

