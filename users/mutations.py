import graphene
from . import types, models
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
        user_id = graphene.String(required=True)

    Output = types.FollowUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        user_id = kwargs.get("user_id")
        try:
            user_to_follow = models.User.objects.get(id=user_id)
            user.following.add(user_to_follow)
            user.save()
            return types.FollowUserResponse(following=user_to_follow)

        except models.User.DoesNotExist:
            return types.FollowUserResponse(following=None)


class UnfollowUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)

    Output = types.UnfollowUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        user_id = kwargs.get("user_id")
        try:
            user_to_unfollow = models.User.objects.get(id=user_id)
            user.following.remove(user_to_unfollow)
            user.save()
            return types.UnfollowUserResponse(following=user_to_unfollow)

        except models.User.DoesNotExist:
            return types.UnfollowUserResponse(following=None)


class AddSports(graphene.Mutation):
    class Arguments:
        sport_ids = graphene.List(graphene.String, required=True)

    Output = types.AddSportsResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_ids = kwargs.get("sport_ids")

        user.add_sports(sport_ids)
        user.save()

        return types.AddSportsResponse(ok=True)


class RemoveSports(graphene.Mutation):
    class Arguments:
        sport_ids = graphene.List(graphene.String, required=True)

    Output = types.AddSportsResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_ids = kwargs.get("sport_ids")

        user.remove_sports(sport_ids)
        user.save()

        return types.RemoveSportsResponse(ok=True)


class UpdateUser(graphene.Mutation):
    class Arguments:
        bio = graphene.String()
        password = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        user_img = Upload()

    Output = types.UpdateUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        bio = kwargs.get("bio")
        first_name = kwargs.get("first_name", "")
        last_name = kwargs.get("last_name", "")
        password = kwargs.get("password", "")
        user_img = kwargs.get("user_img", None)
        if first_name != "":
            user.first_name = first_name

        if last_name != "":
            user.last_name = last_name

        if password != "":
            user.set_password(password)

        if bio is not None:
            user.bio = bio

        if user_img is not None:
            user.user_img = user_img

        user.save()

        return types.UpdateUserResponse(user=user)


class UpdateSports(graphene.Mutation):
    class Arguments:
        sport_ids = graphene.List(graphene.String, required=True)

    Output = types.UpdateSportsResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_ids = kwargs.get("sport_ids")

        ups = models.UserPlaysSport.objects.filter(user=user)
        user_sport_ids = [obj.sport.id for obj in ups]

        to_add = [s_id for s_id in sport_ids if s_id not in user_sport_ids]
        to_remove = [s_id for s_id in user_sport_ids if s_id not in sport_ids]

        user.add_sports(to_add)
        user.remove_sports(to_remove)
        user.save()

        return types.UpdateSportsResponse(user=user)


class RateUserSport(graphene.Mutation):
    class Arguments:
        user_id = graphene.String(required=True)
        sport_id = graphene.String(required=True)
        rating = graphene.Int(required=True)

    Output = types.RateUserSportResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        user_id = kwargs.get("user_id")
        sport_id = kwargs.get("sport_id")
        rating = kwargs.get("rating")

        user.rate_user_sport(user_id, sport_id, rating)
        user.save()

        return types.RateUserSportResponse(ok=True)
