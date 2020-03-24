import graphene
from . import types


class TeamMutation(graphene.Mutation):

    Output = types.TeamMutationReponse

    def mutate(self, info, **kwargs):
        return types.TeamMutationReponse(ok=True)
