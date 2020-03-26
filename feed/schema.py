import graphene
from . import types, queries, mutations


class Query(object):
    my_feed = graphene.Field(
        types.MyFeedResponse,
        resolver=queries.resolve_my_feed,
        required=True,
        args={"page_num": graphene.Int()},
    )
    user_feed = graphene.Field(
        types.UserFeedResponse,
        resolver=queries.resolve_user_feed,
        required=True,
        args={"uuid": graphene.String(required=True), "page_num": graphene.Int()},
    )
    main_feed = graphene.Field(
        types.MainFeedResponse,
        resolver=queries.resolve_main_feed,
        required=True,
        args={"page_num": graphene.Int()},
    )


class Mutation(object):

    create_post = mutations.CreatePost.Field(required=True)
    upvote_post = mutations.UpvotePost.Field(required=True)
    downvote_post = mutations.DownvotePost.Field(required=True)
    remove_post_interaction = mutations.RemovePostInteraction.Field(required=True)
