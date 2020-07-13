import graphene
from graphql_jwt.decorators import login_required
from users import models as user_models
from sports import models as sport_models
from . import types, models


class CreateTeam(graphene.Mutation):
    class Arguments:
        team_name = graphene.String(required=True)
        sport_id = graphene.String(required=True)
        member_ids = graphene.List(graphene.String)

    Output = types.CreateTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_name = kwargs.get("team_name")
        sport_id = kwargs.get("sport_id")
        member_ids = kwargs.get("member_ids")
        try:
            sport = sport_models.Sport.objects.get(id=sport_id)
            team = models.Team.objects.create(
                team_name=team_name, sport=sport, created_by=user
            )
            tm = models.TeamMember.objects.create(user=user, team=team, is_admin=True)
            new_members = user_models.User.objects.filter(id__in=member_ids)
            for member in new_members:
                if member.id != user.id:
                    models.TeamMember.objects.create(user=member, team=team)

            return types.CreateTeamResponse(ok=True)

        except sport_models.Sport.DoesNotExist:
            return types.CreateTeamResponse(ok=False)


class AddTeamMember(graphene.Mutation):
    class Arguments:
        team_id = graphene.String()
        user_id = graphene.String()
        is_admin = graphene.Boolean()

    Output = types.AddTeamMemberResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        user_id = kwargs.get("user_id")
        is_admin = kwargs.get("is_admin")

        try:
            team = models.Team.objects.get(id=team_id)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            try:
                new_member = user_models.User.objects.get(id=user_id)
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
        team_id = graphene.String()
        user_id = graphene.String()

    Output = types.RemoveTeamMemberResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        user_id = kwargs.get("user_id")

        try:
            team = models.Team.objects.get(id=team_id)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            try:
                user_to_remove = user_models.User.objects.get(id=user_id)
                tm = models.TeamMember.objects.get(user=user_to_remove, team=team)
                tm.delete()
                return types.RemoveTeamMemberResponse(ok=True)

            except user_models.User.DoesNotExist:
                return types.RemoveTeamMemberResponse(ok=False)

        except models.Team.DoesNotExist:
            return types.RemoveTeamMemberResponse(ok=False)


class UpdateTeam(graphene.Mutation):
    class Arguments:
        team_id = graphene.String(required=True)
        team_name = graphene.String(required=True)
        sport_id = graphene.String(required=True)
        member_ids = graphene.List(graphene.String)

    Output = types.UpdateTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        team_name = kwargs.get("team_name", None)
        sport_id = kwargs.get("sport_id", None)
        member_ids = kwargs.get("member_ids", [])

        try:
            team = models.Team.objects.get(id=team_id)
            if not user.is_team_admin(team=team):
                raise Exception("Not authorized to edit team.")

            team.update_profile(team_name=team_name, sport_id=sport_id)
            team_member_ids = team.get_member_ids()
            to_add = [m_id for m_id in member_ids if m_id not in team_member_ids]
            to_remove = [m_id for m_id in team_member_ids if m_id not in member_ids]
            team.add_members(to_add)
            team.remove_members(to_remove)
            team.save()
            return types.UpdateTeamResponse(team=team)

        except models.Team.DoesNotExist:
            return types.UpdateTeamResponse(team=None)


class RateTeam(graphene.Mutation):
    class Arguments:
        team_id = graphene.String(required=True)
        rating = graphene.Int(required=True)

    Output = types.RatesTeamResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        team_id = kwargs.get("team_id")
        rating = kwargs.get("rating")

        user.rate_team(team_id, rating)
        user.save()

        return types.RatesTeamResponse(ok=True)
