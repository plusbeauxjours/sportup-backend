import graphene
from . import types


class PostMutation(graphene.Mutation):

    Output = types.PostMutationReponse

    def mutate(self, info, **kwargs):
        return types.PostMutationReponse(ok=True)
