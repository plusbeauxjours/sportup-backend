import graphene
from . import types, queries, mutations


class Query(object):
    me = graphene.Field(types.MeReponse, resolver=queries.resolve_me, required=True)
    get_user = graphene.Field(
        types.GetUserReponse, resolver=queries.resolve_get_user, required=True
    )


class Mutation(object):

    create_user = mutations.CreateUser.Field(required=True)
    follow_user = mutations.FollowUser.Field(required=True)
    unfollow_user = mutations.UnfollowUser.Field(required=True)
    add_sports = mutations.AddSports.Field(required=True)
    remove_sports = mutations.RemoveSports.Field(required=True)

