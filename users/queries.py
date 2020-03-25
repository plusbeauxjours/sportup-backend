from . import types
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required


@login_required
def resolve_me(self, info):
    user = info.context.user

    return types.MeReponse(user=user)


@login_required
def resolve_get_user(self, info, **kwargs):

    uuid = kwargs.get("uuid")

    try:
        user = User.objects.get(uuid=uuid)
        return types.GetUserReponse(user=user)

    except User.DoesNotExist:
        return types.GetUserReponse(user=None)
