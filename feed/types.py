import graphene
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from . import models


class PostType(DjangoObjectType):
    class Meta:
        model = models.Post

    @login_required
    def resolve_interaction(self, info):
        user = info.context.user
        try:
            upi = models.UserPostInteraction.objects.get(post=self, user=user)
            return upi.interaction
        except models.UserPostInteraction.ObjectDoesNotExist:
            return ""


class PostQueryReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class PostMutationReponse(graphene.ObjectType):
    ok = graphene.Boolean()


class MyFeedResponse(graphene.ObjectType):
    feeds = graphene.List(PostType, page_num=graphene.Int())
