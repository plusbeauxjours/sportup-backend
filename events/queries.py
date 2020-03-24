from . import types
from graphql_jwt.decorators import login_required


@login_required
def resolve_event_query(self, info, **kwargs):
    return types.EventQueryReponse(ok=True)
