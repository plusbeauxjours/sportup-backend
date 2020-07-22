from . import types, models
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_team(self, info, **kwargs):
    team_id = kwargs.get("team_id", None)
    if team_id:
        team = models.Team.objects.get(id=team_id)
        return types.GetTeamResponse(team=team)
    else:
        return types.GetTeamResponse(team=None)


@login_required
def resolve_get_teams_for_game(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    sport_ids = kwargs.get("sport_ids", [])
    user = info.context.user

    if sport_ids == []:
        teams = models.Team.objects.exclude(members__id=user.id)

    else:
        teams = models.Team.objects.exclude(members__id=user.id).filter(
            sport__pk__in=sport_ids
        )

    pg = Paginator(teams, 7)
    teams = pg.get_page(page_num)
    if page_num > pg.num_pages:
        return types.GetTeamsForGameResponse(
            posts=None, page_num=page_num, has_next_page=False
        )
    if page_num + 1 > pg.num_pages:
        has_next_page = False
    else:
        has_next_page = True

        return types.GetTeamsForGameResponse(
            teams=teams, page_num=page_num, has_next_page=has_next_page
        )


@login_required
def resolve_get_teams_for_player(self, info, **kwargs):
    user = info.context.user
    user_id = kwargs.get("user_id")
    sport_ids = kwargs.get("sport_ids", [])

    if sport_ids == []:
        teams = models.Team.objects.exclude(members__id=user.id).filter(
            created_by__id=user_id
        )
        return types.GetTeamsForPlayerResponse(teams=teams)
    else:
        teams = models.Team.objects.exclude(members__id=user.id).filter(
            sport__pk__in=sport_ids, created_by__id=user_id
        )
        return types.GetTeamsForPlayerResponse(teams=teams)


def resolve_get_search_teams(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    if search_text == "":
        return types.GetSearchTeamsResponse(teams=None)
    else:
        teams = models.Team.objects.filter(team_name__icontains=search_text)[:5]
        return types.GetSearchTeamsResponse(teams=teams)
