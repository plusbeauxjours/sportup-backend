from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_all_sports(self, info):
    sports = models.Sport.objects.all()
    return types.AllSportReponse(sports=sports)
