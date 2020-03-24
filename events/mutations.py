import graphene
from . import types


class EventMutation(graphene.Mutation):

    Output = types.EventMutationReponse

    def mutate(self, info, **kwargs):
        return types.EventMutationReponse(ok=True)
