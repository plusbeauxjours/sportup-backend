import graphene
from . import types


class ProfileMutation(graphene.Mutation):

    Output = types.ProfileMutationReponse

    def mutate(self, info, **kwargs):
        return types.ProfileMutationReponse(ok=True)
