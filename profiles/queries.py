from . import types
from graphql_jwt.decorators import login_required


@login_required
def resolve_profile_query(self, info, **kwargs):
    return types.ProfileQueryReponse(ok=True)
