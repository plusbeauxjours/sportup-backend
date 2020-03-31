import graphene
from . import types, models
from sports import models as sport_models


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        sport_id = graphene.Int(required=True)
        start_date = graphene.Date()
        end_date = graphene.Date()
        start_time = graphene.Time()
        end_time = graphene.Time()
        minimum_members = graphene.Int(required=True)
        maximum_members = graphene.Int(required=True)
        expected_teams = graphene.Int()

    Output = types.CreateEventReponse

    def mutate(self, info, **kwargs):
        user = info.context.user
        name = kwargs.get("name")
        description = kwargs.get("description", None)
        sport_id = kwargs.get("sport_id")
        start_date = kwargs.get("start_date", None)
        end_date = kwargs.get("end_date", None)
        start_time = kwargs.get("start_time", None)
        end_time = kwargs.get("end_time", None)
        minimum_members = kwargs.get("minimum_members")
        maximum_members = kwargs.get("maximum_members")
        expected_teams = kwargs.get("expected_teams", 0)

        try:
            sport = sport_models.Sport.objects.get(pk=sport_id)
            event = models.Event.objects.create(
                owner=user,
                name=name,
                description=description,
                sport=sport,
                start_date=start_date,
                end_date=end_date,
                start_time=start_time,
                end_time=end_time,
                minimum_members=minimum_members,
                maximum_members=maximum_members,
                expected_teams=expected_teams,
            )

            return types.CreateEventReponse(event=event)

        except sport_models.Sport.DoesNotExist:
            return types.CreateEventReponse(event=None)
