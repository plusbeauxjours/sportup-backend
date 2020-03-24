from . import types
from graphql_jwt.decorators import login_required


@login_required
def resolve_post_query(self, info, **kwargs):
    return types.PostQueryReponse(ok=True)
