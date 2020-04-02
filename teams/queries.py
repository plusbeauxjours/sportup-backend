from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_team(self, info, **kwargs):
    id = kwargs.get("id", None)

    if id:
        team = models.Team.objects.get(pk=id)

        return types.GetTeamResponse(team=team)


@login_required
def resolve_get_teams_for_game(self, info, **kwargs):
    user = info.context.user
    sport_ids = kwargs.get("sport_ids", [])

    if sport_ids == []:
        teams = models.Team.objects.exclude(members__uuid=user.uuid)
        return types.GetTeamsForGameResponse(teams=teams)

    teams = models.Team.objects.exclude(members__uuid=user.uuid).filter(
        sport__pk__in=sport_ids
    )

    return types.GetTeamsForGameResponse(teams=teams)
