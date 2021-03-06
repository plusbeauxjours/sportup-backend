import graphene
from . import types, queries, mutations


class Query(object):
    me = graphene.Field(types.MeReponse, resolver=queries.resolve_me, required=True)
    get_user = graphene.Field(
        types.GetUserReponse,
        resolver=queries.resolve_get_user,
        required=True,
        args={"user_id": graphene.String(required=True),},
    )
    get_user_from_username = graphene.Field(
        types.GetUserFromUsernameReponse,
        resolver=queries.resolve_get_user_from_username,
        required=True,
        args={"username": graphene.String(required=True),},
    )
    get_users_for_game = graphene.Field(
        types.GetUsersForGamesResponse,
        resolver=queries.resolve_get_users_for_games,
        required=True,
        args={
            "page_num": graphene.Int(),
            "sport_ids": graphene.List(graphene.String, required=True),
        },
    )
    get_search_users = graphene.Field(
        types.GetSearchUsersResponse,
        resolver=queries.resolve_get_search_users,
        required=True,
        args={"search_text": graphene.String(required=True),},
    )


class Mutation(object):
    create_user = mutations.CreateUser.Field(required=True)
    follow_user = mutations.FollowUser.Field(required=True)
    unfollow_user = mutations.UnfollowUser.Field(required=True)
    add_sports = mutations.AddSports.Field(required=True)
    remove_sports = mutations.RemoveSports.Field(required=True)
    update_user = mutations.UpdateUser.Field(required=True)
    update_sports = mutations.UpdateSports.Field(required=True)
    rate_user_sport = mutations.RateUserSport.Field(required=True)
    register_push = mutations.RegisterPush.Field(required=True)
    facebook_connect = mutations.FacebookConnect.Field(required=True)
    apple_connect = mutations.AppleConnect.Field(required=True)