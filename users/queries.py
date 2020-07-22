from . import types, models
from django.db.models import Q
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required


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

    page_num = kwargs.get("page_num", 1)
    sport_ids = kwargs.get("sport_ids", [])
    user = info.context.user

    if sport_ids == []:
        users = models.User.objects.exclude(id=user.id)
    else:
        users = models.User.objects.exclude(id=user.id).filter(sports__id__in=sport_ids)

    pg = Paginator(users, 7)
    if page_num > pg.num_pages:
        return types.GetUsersForGamesResponse(
            posts=None, page_num=page_num, has_next_page=False
        )
    if page_num + 1 > pg.num_pages:
        has_next_page = False
    else:
        has_next_page = True

        return types.GetUsersForGamesResponse(
            users=users, page_num=page_num, has_next_page=has_next_page
        )


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
