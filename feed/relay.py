import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    my_feed = DjangoFilterConnectionField(PostNode)

    @login_required
    def resovle_my_feed(self, info):
        user = info.context.user
        uf = Post.objects.filter(posted_by=user)
        return uf
