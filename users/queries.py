from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_me(self, info):
    user = info.context.user

    return types.MeReponse(user=user)


@login_required
def resolve_get_user(self, info, **kwargs):

    uuid = kwargs.get("uuid")

    try:
        user = models.User.objects.get(uuid=uuid)
        return types.GetUserReponse(user=user)

    except models.User.DoesNotExist:
        return types.GetUserReponse(user=None)
