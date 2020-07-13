import graphene
from graphene import relay
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from . import models


class PostType(DjangoObjectType):
    interaction = graphene.String()

    class Meta:
        model = models.Post

    @login_required
    def resolve_interaction(self, info):
        user = info.context.user
        try:
            upi = models.UserPostInteraction.objects.get(post=self, user=user)
            return upi.interaction
        except models.UserPostInteraction.DoesNotExist:
            return ""


class GetMyFeedResponse(graphene.ObjectType):
    posts = graphene.List(PostType, page_num=graphene.Int())
    page_num = graphene.Int()
    has_next_page = graphene.Boolean()


class GetUserFeedResponse(graphene.ObjectType):
    posts = graphene.List(PostType, page_num=graphene.Int())
    page_num = graphene.Int()
    has_next_page = graphene.Boolean()


class GetMainFeedResponse(graphene.ObjectType):
    posts = graphene.List(PostType, page_num=graphene.Int())
    page_num = graphene.Int()
    has_next_page = graphene.Boolean()


class CreatePostReponse(graphene.ObjectType):
    post = graphene.Field(PostType)


class UpvotePostResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class DownvotePostResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RemovePostInteractionResponse(graphene.ObjectType):
    ok = graphene.Boolean()
