from . import mutations


class Mutation(object):

    create_user = mutations.CreateUser.Field(required=True)
