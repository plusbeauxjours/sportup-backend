from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_team(self, info, **kwargs):
    uuid = kwargs.get("uuid", None)

    if uuid:
        team = models.Team.objects.get(uuid=uuid)

        return types.GetTeamResponse(team=team)


@login_required
def resolve_get_teams_for_game(self, info, **kwargs):
    user = info.context.user
    sport_uuids = kwargs.get("sport_uuids", [])

    if sport_uuids == []:
        teams = models.Team.objects.exclude(members__uuid=user.uuid)
        return types.GetTeamsForGameResponse(teams=teams)

    teams = models.Team.objects.exclude(members__uuid=user.uuid).filter(
        sport__pk__in=sport_uuids
    )

    return types.GetTeamsForGameResponse(teams=teams)


def resolve_get_search_teams(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    teams = models.Team.objects.filter(name__icontains=search_text)[:5]
    return types.GetSearchTeamsResponse(teams=teams)
