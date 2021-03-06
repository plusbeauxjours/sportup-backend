import graphene
from . import types, queries, mutations


class Query(object):
    get_team = graphene.Field(
        types.GetTeamResponse,
        resolver=queries.resolve_get_team,
        required=True,
        args={"team_id": graphene.String(),},
    )
    get_teams_for_game = graphene.Field(
        types.GetTeamsForGameResponse,
        resolver=queries.resolve_get_teams_for_game,
        required=True,
        args={"page_num": graphene.Int(), "sport_ids": graphene.List(graphene.String),},
    )
    get_search_teams = graphene.Field(
        types.GetSearchTeamsResponse,
        resolver=queries.resolve_get_search_teams,
        required=True,
        args={"search_text": graphene.String(required=True),},
    )
    get_teams_for_player = graphene.Field(
        types.GetTeamsForPlayerResponse,
        resolver=queries.resolve_get_teams_for_player,
        required=True,
        args={
            "user_id": graphene.String(),
            "sport_ids": graphene.List(graphene.String),
        },
    )


class Mutation(object):
    create_team = mutations.CreateTeam.Field(required=True)
    add_team_member = mutations.AddTeamMember.Field(required=True)
    remove_team_member = mutations.RemoveTeamMember.Field(required=True)
    update_team = mutations.UpdateTeam.Field(required=True)
    rate_team = mutations.RateTeam.Field(required=True)
