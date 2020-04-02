import graphene
from . import types, queries, mutations


class Query(object):
    team_query = graphene.Field(
        types.TeamQueryReponse,
        resolver=queries.resolve_team_query,
        required=True,
        args={},
    )


class Mutation(object):
    create_team = mutations.CreateTeam.Field(required=True)
    add_team_member = mutations.AddTeamMember.Field(required=True)
    remove_team_member = mutations.RemoveTeamMember.Field(required=True)
    update_team = mutations.UpdateTeam.Field(required=True)
