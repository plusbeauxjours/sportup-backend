from . import types, models
from django.db.models import Q
from graphql_jwt.decorators import login_required


@login_required
def resolve_me(self, info):
    user = info.context.user
    return types.MeReponse(user=user)


@login_required
def resolve_get_user(self, info, **kwargs):
    user_id = kwargs.get("user_id", "")

    try:
        user = models.User.objects.get(id=user_id)
        return types.GetUserReponse(user=user)

    except models.User.DoesNotExist:
        return types.GetUserReponse(user=None)


@login_required
def resolve_get_user_from_username(self, info, **kwargs):
    username = kwargs.get("username", "")

    try:
        user = models.User.objects.get(username=username)
        return types.GetUserReponse(user=user)

    except models.User.DoesNotExist:
        return types.GetUserReponse(user=None)


@login_required
def resolve_get_users_for_games(self, info, **kwargs):
    user = info.context.user
    sport_ids = kwargs.get("sport_ids", [])
    if sport_ids == []:
        users = models.User.objects.exclude(id=user.id)
        return types.GetUsersForGamesResponse(users=users)
    else:
        users = models.User.objects.exclude(id=user.id).filter(sports__id__in=sport_ids)
        return types.GetUsersForGamesResponse(users=users)


def resolve_get_search_users(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    if search_text == "":
        return types.GetSearchUsersResponse(users=None)
    else:
        search_first_names = Q(first_name__istartswith=search_text)
        search_last_names = Q(last_name__istartswith=search_text)
        search_username = Q(username__istartswith=search_text)
        users = models.User.objects.filter(
            search_first_names | search_last_names | search_username
        )[:7]
        return types.GetSearchUsersResponse(users=users)
