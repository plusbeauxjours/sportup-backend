import graphene
from . import models
from django.core.paginator import Paginator
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserPlaysSportType(DjangoObjectType):
    sport_id = graphene.Int()
    name = graphene.String()

    class Meta:
        model = models.UserPlaysSport

    def resolve_sport_id(self, info):
        return self.sport.id

    def resolve_name(self, info):
        return self.sport.name


class FollowType(DjangoObjectType):
    class Meta:
        model = models.User


class UserType(DjangoObjectType):
    is_following = graphene.Boolean()
    sports = graphene.List(UserPlaysSportType)
    followers = graphene.List(FollowType, page_num=graphene.Int())
    following = graphene.List(FollowType, page_num=graphene.Int())
    followers_count = graphene.Int(source="followers_count")
    following_count = graphene.Int(source="following_count")

    class Meta:
        model = models.User

    @login_required
    def resolve_is_following(self, info):
        user = info.context.user
        try:
            f = user.following.get(pk=self.pk)
            return True
        except models.User.DoesNotExist:
            return False

    def resolve_sports(self, info, **kwargs):
        return self.UserPlaysSport_user.all()

    def resolve_followers(self, info, **kwargs):
        page_num = kwargs.get("page_num", 1)
        qs = models.User.objects.filter(id__in=self.user.followers.all())
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)

    def resolve_following(self, info, **kwargs):
        page_num = kwargs.get("page_num", 1)
        qs = self.following.all()
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)


class MeReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class GetUserReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class CreateUserReponse(graphene.ObjectType):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)


class FollowUserResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class UnfollowUserResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class AddSportsResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RemoveSportsResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class UpdateUserResponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class UpdateSportsResponse(graphene.ObjectType):
    user = graphene.Field(UserType)
