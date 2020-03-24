import graphene
from . import types


class SportMutation(graphene.Mutation):

    Output = types.SportMutationReponse

    def mutate(self, info, **kwargs):
        return types.SportMutationReponse(ok=True)
