from . import types
from graphql_jwt.decorators import login_required


@login_required
def resolve_sport_query(self, info, **kwargs):
    return types.SportQueryReponse(ok=True)
