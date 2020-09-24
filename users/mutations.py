import graphene
import random
import json
from . import types, models
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token
from graphql_jwt.decorators import login_required


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
            user.follow_user(user_to_follow)
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
            user.unfollow_user(user_to_unfollow)
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

    Output = types.UpdateUserResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        bio = kwargs.get("bio")
        first_name = kwargs.get("first_name", "")
        last_name = kwargs.get("last_name", "")
        password = kwargs.get("password", "")
        if first_name != "":
            user.first_name = first_name

        if last_name != "":
            user.last_name = last_name

        if password != "":
            user.set_password(password)

        if bio is not None:
            user.bio = bio

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
        ups_ids = [obj.sport.id for obj in ups]

        to_add = [int(s_id) for s_id in sport_ids if int(s_id) not in ups_ids]
        to_remove = [s_id for s_id in ups_ids if str(s_id) not in sport_ids]
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


class RegisterPush(graphene.Mutation):
    class Arguments:
        push_token = graphene.String(required=True)

    Output = types.RegisterPushResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        push_token = kwargs.get("push_token")
        if user.push_token == push_token:
            return types.RegisterPushResponse(ok=True)
        else:
            user.push_token = push_token
            user.save()
            return types.RegisterPushResponse(ok=True)


class AppleConnect(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        apple_id = graphene.String(required=True)

    Output = types.AppleConnectResponse

    def mutate(self, info, **kwargs):

        first_name = kwargs.get("first_name", "")
        last_name = kwargs.get("last_name", "")
        email = kwargs.get("email", "")
        apple_id = kwargs.get("apple_id", "")

        try:
            user = models.User.objects.get(apple_id=apple_id)
            token = get_token(user)
            return types.AppleConnectResponse(ok=True, token=token)

        except models.User.DoesNotExist:
            with open(
                "users/adjectives.json", mode="rt", encoding="utf-8"
            ) as adjectives:
                with open("users/nouns.json", mode="rt", encoding="utf-8") as nouns:
                    adjectives = json.load(adjectives)
                    nouns = json.load(nouns)
                    if email != "":
                        local, at, domain = email.rpartition("@")
                        username = random.choice(adjectives) + local.capitalize()
                    else:
                        username = (
                            random.choice(adjectives)
                            + random.choice(nouns).capitalize()
                        )

                    user = models.User.objects.create_user(username)
                    if first_name != "":
                        user.first_name = first_name
                    if last_name != "":
                        user.last_name = last_name
                    if apple_id != "":
                        user.apple_id = apple_id
                    if email != "":
                        user.email = email
                    user.has_apple_account = True
                    user.save()

                    token = get_token(user)
                    return types.AppleConnectResponse(ok=True, token=token)


class FacebookConnect(graphene.Mutation):
    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        fb_id = graphene.String(required=True)

    Output = types.FacebookConnectResponse

    def mutate(self, info, **kwargs):

        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        email = kwargs.get("email")
        fb_id = kwargs.get("fb_id")

        try:
            user = models.User.objects.get(fb_id=fb_id)
            token = get_token(user)
            return types.FacebookConnectResponse(ok=True, token=token)

        except models.User.DoesNotExist:
            with open(
                "users/adjectives.json", mode="rt", encoding="utf-8"
            ) as adjectives:
                with open("users/nouns.json", mode="rt", encoding="utf-8") as nouns:
                    adjectives = json.load(adjectives)
                    nouns = json.load(nouns)
                    if email != "":
                        local, at, domain = email.rpartition("@")
                        username = random.choice(adjectives) + local.capitalize()
                    else:
                        username = (
                            random.choice(adjectives)
                            + random.choice(nouns).capitalize()
                        )

                    user = models.User.objects.create_user(username)
                    if first_name != "":
                        user.first_name = first_name
                    if last_name != "":
                        user.last_name = last_name
                    if fb_id != "":
                        user.fb_id = fb_id
                    if email != "":
                        user.email = email
                    user.has_apple_account = True
                    user.save()

                    token = get_token(user)
                    return types.AppleConnectResponse(ok=True, token=token)
