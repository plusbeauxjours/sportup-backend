import graphene
from graphql_jwt.decorators import login_required
from users import models as user_models
from sports import models as sport_models
from . import types, models


class CreateTeam(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        sport_id = graphene.Int(required=True)
        member_uuids = graphene.List(graphene.String)

    Output = types.CreateTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        name = kwargs.get("name")
        sport_id = kwargs.get("sport_id")
        member_uuids = kwargs.get("member_uuids")

        try:
            sport = sport_models.Sport.objects.get(pk=sport_id)
            team = models.Team.objects.create(name=name, sport=sport, created_by=user)
            tm = models.TeamMember.objects.create(user=user, team=team, is_admin=True)

            new_members = user_models.User.objects.filter(uuid__in=member_uuids)
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


class RemoveTeamMember(graphene.Mutation):
    class Arguments:
        team_id = graphene.Int()
        uuid = graphene.String()

    Output = types.RemoveTeamMemberResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        uuid = kwargs.get("uuid")

        try:
            team = models.Team.objects.get(pk=team_id)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            try:
                user_to_remove = user_models.User.objects.get(uuid=uuid)
                tm = models.TeamMember.objects.get(user=user_to_remove, team=team)
                tm.delete()
                return types.RemoveTeamMemberResponse(ok=True)

            except user_models.User.DoesNotExist:
                return types.RemoveTeamMemberResponse(ok=False)

        except models.Team.DoesNotExist:
            return types.RemoveTeamMemberResponse(ok=False)


class UpdateTeam(graphene.Mutation):
    class Arguments:
        team_id = graphene.Int()
        name = graphene.String()
        sport_id = graphene.Int()
        member_uuids = graphene.List(graphene.String)

    Output = types.UpdateTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        name = kwargs.get("name", None)
        sport_id = kwargs.get("sport_id", None)
        member_uuids = kwargs.get("member_uuids", [])

        try:
            team = models.Team.objects.get(pk=team_id)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            team.update_profile(name=name, sport_id=sport_id)
            team_member_uuids = team.get_member_uuids()
            to_add = [
                m_uuid for m_uuid in member_uuids if m_uuid not in team_member_uuids
            ]
            to_remove = [
                m_uuid for m_uuid in team_member_uuids if m_uuid not in member_uuids
            ]
            print("to_add", to_add)
            print("to_remove", to_remove)

            team.add_members(to_add)
            team.remove_members(to_remove)
            team.save()
            return types.UpdateTeamResponse(team=team)

        except models.Team.DoesNotExist:
            return types.UpdateTeamResponse(team=None)


class RateTeam(graphene.Mutation):
    class Arguments:
        team_id = graphene.Int(required=True)
        rating = graphene.Int(required=True)

    Output = types.RatesTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        rating = kwargs.get("rating")

        team = models.Team.objects.get(pk=team_id)

        try:
            urt = models.UserRatesTeam.objects.get(user=user, team=team)
            urt.rating = rating
            urt.save()
            return types.RatesTeamResponse(ok=True)

        except models.UserRatesTeam.DoesNotExist:
            new_urt = models.UserRatesTeam.objects.create(
                user=user, team=team, rating=rating
            )
            return types.RatesTeamResponse(ok=True)

