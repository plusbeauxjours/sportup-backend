from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_me(self, info):
    user = info.context.user
    return types.MeReponse(user=user)


@login_required
def resolve_get_user(self, info, **kwargs):
    uuid = kwargs.get("uuid")

    try:
        user = models.User.objects.get(uuid=uuid)
        return types.GetUserReponse(user=user)

    except models.User.DoesNotExist:
        return types.GetUserReponse(user=None)


@login_required
def resolve_users_for_games(self, info, **kwargs):
    user = info.context.user
    sport_ids = kwargs.get("sport_ids", [])

    if sport_ids == []:
        users = models.User.objects.exclude(pk=user.id)
        return types.UsersForGamesResponse(users=users)

    users = models.User.objects.exclude(pk=user.id).filter(sports__pk__in=sport_ids)
    return types.UsersForGamesResponse(users=users)
