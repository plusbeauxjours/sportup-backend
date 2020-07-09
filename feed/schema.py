import graphene
from . import types, queries, mutations


class Query(object):
    get_my_feed = graphene.Field(
        types.GetMyFeedResponse,
        resolver=queries.resolve_get_my_feed,
        required=True,
        args={"page_num": graphene.Int()},
    )
    get_user_feed = graphene.Field(
        types.GetUserFeedResponse,
        resolver=queries.resolve_get_user_feed,
        required=True,
        args={"user_id": graphene.String(required=True), "page_num": graphene.Int()},
    )
    get_main_feed = graphene.Field(
        types.GetMainFeedResponse,
        resolver=queries.resolve_get_main_feed,
        required=True,
        args={"page_num": graphene.Int()},
    )


class Mutation(object):
    create_post = mutations.CreatePost.Field(required=True)
    upvote_post = mutations.UpvotePost.Field(required=True)
    downvote_post = mutations.DownvotePost.Field(required=True)
    remove_post_interaction = mutations.RemovePostInteraction.Field(required=True)
