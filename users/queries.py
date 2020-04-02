from . import types, models
from django.db.models import Q
from graphql_jwt.decorators import login_required


@login_required
def resolve_me(self, info):
    user = info.context.user
    return types.MeReponse(user=user)


@login_required
def resolve_get_user(self, info, **kwargs):
    uuid = kwargs.get("uuid", "")

    try:
        user = models.User.objects.get(uuid=uuid)
        return types.GetUserReponse(user=user)

    except models.User.DoesNotExist:
        return types.GetUserReponse(user=None)


@login_required
def resolve_get_users_for_games(self, info, **kwargs):
    user = info.context.user
    sport_ids = kwargs.get("sport_ids", [])

    if sport_ids == []:
        users = models.User.objects.exclude(pk=user.id)
        return types.GetUsersForGamesResponse(users=users)

    users = models.User.objects.exclude(pk=user.id).filter(sports__pk__in=sport_ids)
    return types.GetUsersForGamesResponse(users=users)


def resolve_get_search_users(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    search_first_names = Q(first_name__icontains=search_text)
    search_last_names = Q(last_name__icontains=search_text)
    search_username = Q(username__icontains=search_text)
    users = models.User.objects.filter(
        search_first_names | search_last_names | search_username
    )[:7]
    return types.GetSearchUsersResponse(users=users)
