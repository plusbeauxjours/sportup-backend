import graphene
from . import types, models
from graphql_jwt.decorators import login_required
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

    Output = types.CreateEventResponse

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

            return types.CreateEventResponse(event=event)

        except sport_models.Sport.DoesNotExist:
            return types.CreateEventResponse(event=None)


class RegisterTeam(graphene.Mutation):
    class Arguments:
        event_id = graphene.Int(required=True)
        team_name = graphene.String(required=True)
        captain_name = graphene.String(required=True)
        captain_cnic = graphene.String(required=True)
        captain_contact = graphene.String(required=True)
        player_names = graphene.List(graphene.String)

    Output = types.RegisterTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        event_id = kwargs.get("event_id")
        team_name = kwargs.get("team_name")
        captain_name = kwargs.get("captain_name")
        captain_cnic = kwargs.get("captain_cnic")
        captain_contact = kwargs.get("captain_contact")
        player_names = kwargs.get("player_names")

        try:
            event = models.Event.objects.get(pk=event_id)
            registration = models.Registration.objects.create(
                name=team_name,
                event=event,
                registered_by=user,
                captain_name=captain_name,
                captain_cnic=captain_cnic,
                captain_contact_num=captain_contact,
            )

            for name in player_names:
                models.RegisteredPlayer.objects.create(
                    name=name, registration=registration
                )

            return types.RegisterTeamResponse(ok=True)

        except models.Event.DoesNotExist:
            return types.RegisterTeamResponse(ok=False)


class ApproveRegistration(graphene.Mutation):
    class Arguments:
        registration_id = graphene.Int(required=True)

    Output = types.ApproveRegistrationResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        registration_id = kwargs.get("registration_id")

        try:
            registration = models.Registration.objects.get(pk=registration_id)
            if registration.event.owner != user:
                raise Exception("Not authorized to edit event!")

            registration.approved = True
            registration.save()
            return types.ApproveRegistrationResponse(ok=True)

        except models.Registration.DoesNotExist:
            return types.ApproveRegistrationResponse(ok=False)


class DisapproveRegistration(graphene.Mutation):
    class Arguments:
        registration_id = graphene.Int(required=True)

    Output = types.DisapproveRegistrationResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        registration_id = kwargs.get("registration_id")

        try:
            registration = models.Registration.objects.get(pk=registration_id)
            if registration.event.owner != user:
                raise Exception("Not authorized to edit event!")

            registration.approved = False
            registration.save()
            return types.DisapproveRegistrationResponse(ok=True)

        except models.Registration.DoesNotExist:
            return types.DisapproveRegistrationResponse(ok=False)
