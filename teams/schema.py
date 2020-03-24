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

    team_mutation = mutations.TeamMutation.Field(required=True)
