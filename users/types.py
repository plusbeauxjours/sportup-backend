import graphene
from . import models
from django.core.paginator import Paginator
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required


class UserPlaysSportType(DjangoObjectType):
    sport_id = graphene.String()
    rating = graphene.Float(source="rating")
    name = graphene.String()

    class Meta:
        model = models.UserPlaysSport

    def resolve_sport_id(self, info):
        return self.sport.id

    def resolve_name(self, info):
        return self.sport.name


class FollowType(DjangoObjectType):
    name = graphene.String()
    is_following = graphene.Boolean()

    class Meta:
        model = models.User

    @login_required
    def resolve_is_following(self, info):
        user = info.context.user
        try:
            user.following.get(id=self.id)
            return True
        except models.User.DoesNotExist:
            return False

    def resolve_name(self, info):
        return self.get_full_name()


class UserType(DjangoObjectType):
    name = graphene.String()
    is_following = graphene.Boolean()
    sports = graphene.List(UserPlaysSportType)
    followers = graphene.List(FollowType, page_num=graphene.Int())
    following = graphene.List(FollowType, page_num=graphene.Int())
    teams_count = graphene.Int()
    followers_count = graphene.Int()
    following_count = graphene.Int()

    class Meta:
        model = models.User

    @login_required
    def resolve_is_following(self, info):
        user = info.context.user
        try:
            user.following.get(id=self.id)
            return True
        except models.User.DoesNotExist:
            return False

    def resolve_following_count(self, info):
        return self.following.count()

    def resolve_followers_count(self, info):
        return self.followers.count()

    def resolve_sports(self, info, **kwargs):
        return self.UserPlaysSport_user.all()

    def resolve_followers(self, info, **kwargs):
        page_num = kwargs.get("page_num", 1)
        qs = self.followers.all()
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)

    def resolve_following(self, info, **kwargs):
        page_num = kwargs.get("page_num", 1)
        qs = self.following.all()
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)

    def resolve_teams_count(self, info):
        return self.team_set.count()

    def resolve_name(self, info):
        return self.get_full_name()


class MeReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class GetUserReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class GetUserFromUsernameReponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class GetUsersForGamesResponse(graphene.ObjectType):
    users = graphene.List(UserType)
    page_num = graphene.Int()
    has_next_page = graphene.Boolean()


class GetSearchUsersResponse(graphene.ObjectType):
    users = graphene.List(UserType)


class CreateUserReponse(graphene.ObjectType):
    ok = graphene.Boolean()
    user = graphene.Field(UserType)


class FollowUserResponse(graphene.ObjectType):
    following = graphene.Field(FollowType)


class UnfollowUserResponse(graphene.ObjectType):
    following = graphene.Field(FollowType)


class AddSportsResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RemoveSportsResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class UpdateUserResponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class UpdateSportsResponse(graphene.ObjectType):
    user = graphene.Field(UserType)


class RateUserSportResponse(graphene.ObjectType):
    ok = graphene.Boolean()


class RegisterPushResponse(graphene.ObjectType):
    ok = graphene.Boolean()
