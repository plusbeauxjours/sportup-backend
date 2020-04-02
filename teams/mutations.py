import graphene
from graphql_jwt.decorators import login_required
from users import models as user_models
from sport import models as sport_models
from . import types, models


class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        sport_id = graphene.Int(rewquired=True)
        member_ids = graphene.List(graphene.String)

    Output = types.CreateTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        sport_id = kwargs.get("sport_id")
        name = kwargs.get("name")
        member_ids = kwargs.get("member_ids")

        try:
            sport = sport_models.Sport.objects.get(pk=sport_id)
            team = models.Team.objects.create(name=name, sport=sport, create_by=user)
            tm = models.TeamMember.objects.create(user=user, team=team, is_admin=True)

            new_members = user_models.User.objects.filter(pk__in=member_ids)
            for member in new_members:
                if member.uuid != user.uuid:
                    models.TeamMember.objects.create(user=member, team=team)

            return types.CreateTeamResponse(user=user)

        except sport_models.Sport.DoesNotExist:
            return types.CreateTeamResponse(user=None)


class AddTeamMember(graphene.Mutation):
    class Arguments:
        team_id = graphene.Int()
        uuid = graphene.String()
        is_admin = graphene.Boolean()

    Output = types.AddTeamMemberResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        uuid = kwargs.get("uuid")
        is_admin = kwargs.get("is_admin")

        try:
            team = models.Team.objects.get(pk=team_id)
            print("team", team)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            try:
                new_member = user_models.User.objects.get(uuid=uuid)
                tm = models.TeamMember.objects.create(
                    team=team, user=new_member, is_admin=is_admin
                )
                return types.AddTeamMemberResponse(ok=True)

            except user_models.User.DoesNotExist:
                return types.AddTeamMemberResponse(ok=False)

        except models.Team.DoesNotExist:
            return types.AddTeamMemberResponse(ok=False)
