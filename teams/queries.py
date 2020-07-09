from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_team(self, info, **kwargs):
    team_id = kwargs.get("team_id", None)

    if team_id:
        team = models.Team.objects.get(id=team_id)

        return types.GetTeamResponse(team=team)


@login_required
def resolve_get_teams_for_game(self, info, **kwargs):
    user = info.context.user
    sport_ids = kwargs.get("sport_ids", [])

    if sport_ids == []:
        teams = models.Team.objects.exclude(members__id=user.id)
        return types.GetTeamsForGameResponse(teams=teams)

    teams = models.Team.objects.exclude(members__id=user.id).filter(
        sport__pk__in=sport_ids
    )

    return types.GetTeamsForGameResponse(teams=teams)


def resolve_get_search_teams(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    teams = models.Team.objects.filter(team_name__icontains=search_text)[:5]
    return types.GetSearchTeamsResponse(teams=teams)
