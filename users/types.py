import graphene
from . import models
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required


class UserPlaysSportType(DjangoObjectType):
    sport_id = graphene.Int()
    name = graphene.String()
    img_url = graphene.String()

    class Meta:
        model = models.UserPlaysSport

    def resolve_sport_id(self, info):
        return self.sport.id

    def resolve_name(self, info):
        return self.sport.name

    def resolve_img_url(self, info):
        return self.sport.img_path


class UserType(DjangoObjectType):
    sports = graphene.List(UserPlaysSportType)
    following_count = graphene.Int()
    followers_count = graphene.Int()
    is_following = graphene.Boolean()

    class Meta:
        model = get_user_model()

    def resolve_sports(self, info):
        return self.userplayssport_set.all()

    def resolve_followers(self, info, page_num=1):
        qs = models.User.objects.filter(profile__in=self.user.followers.all())
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)

    def resolve_following(self, info, page_num=1):
        qs = self.following.all()
        pg = Paginator(qs, 12)
        return pg.get_page(page_num)

    def resolve_following_count(self, info):
        return self.following.count()

    def resolve_followers_count(self, info):
        return self.user.followers.count()

    @login_required
    def resolve_is_following(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("Not authenticated!")

        try:
            f = user.following.get(pk=self.pkd)
            return True
        except models.ObjectDoesNotExist:
            return False


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
