from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_all_sports(self, info):
    sports = models.Sport.objects.all()
    return types.GetAllSportReponse(sports=sports)
