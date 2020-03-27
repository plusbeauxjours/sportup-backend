import graphene
from . import types, models
from sports import models as sport_models
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    Output = types.CreateUserReponse

    def mutate(self, info, **kwargs):
        username = kwargs.get("username")
        password = kwargs.get("password")
        email = kwargs.get("email")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        user = get_user_model()(
            username=username, email=email, first_name=first_name, last_name=last_name,
        )
        user.set_password(password)
        user.save()

        return types.CreateUserReponse(ok=True, user=user)


class FollowUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)

    Output = types.FollowUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        uuid = kwargs.get("uuid")

        try:
            user_to_follow = models.User.objects.get(uuid=uuid)
            user.following.add(user_to_follow)
            user.save()
            return types.FollowUserResponse(ok=True)

        except models.User.DoesNotExist:
            return types.FollowUserResponse(ok=False)


class UnfollowUser(graphene.Mutation):
    class Arguments:
        uuid = graphene.String(required=True)

    Output = types.UnfollowUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        uuid = kwargs.get("uuid")

        try:
            user_to_unfollow = models.User.objects.get(uuid=uuid)
            user.following.remove(user_to_unfollow)
            user.save()
            return types.UnfollowUserResponse(ok=True)

        except models.User.DoesNotExist:
            return types.UnfollowUserResponse(ok=False)


class AddSports(graphene.Mutation):
    class Arguments:
        sport_ids = graphene.List(graphene.Int, required=True)

    Output = types.AddSportsResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_ids = kwargs.get("sport_ids")

        sports = sport_models.Sport.objects.filter(pk__in=sport_ids)
        for sport in sports:
            ups = models.UserPlaysSport.objects.create(user=user, sport=sport)
        user.save()

        return types.AddSportsResponse(ok=True)


class RemoveSports(graphene.Mutation):
    class Arguments:
        sport_ids = graphene.List(graphene.Int, required=True)

    Output = types.AddSportsResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_ids = kwargs.get("sport_ids")

        sports = sport_models.Sport.objects.filter(pk__in=sport_ids)
        models.UserPlaysSport.objects.filter(user=user, sport__in=sports).delete()
        user.save()

        return types.RemoveSportsResponse(ok=True)


class UpdateUser(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        profile_img = Upload()

    Output = types.UpdateUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        bio = kwargs.get("bio")
        first_name = kwargs.get("first_name", "")
        last_name = kwargs.get("last_name", "")
        password = kwargs.get("password", "")
        profile_img = kwargs.get("profile_img", None)

        if first_name != "":
            user.first_name = first_name

        if last_name != "":
            user.last_name = last_name

        if password != "":
            user.set_password(password)

        if bio is not None:
            self.bio = bio

        if profile_img is not None:
            self.profile_img = profile_img

        user.save()

        return types.UpdateUserResponse(user=user)
