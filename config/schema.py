import graphene
import graphql_jwt

from users import schema as user_schema
from teams import schema as team_schema
from feed import schema as feed_schema
from sports import schema as sport_schema
from events import schema as event_schema


class Query(
    user_schema.Query,
    team_schema.Query,
    feed_schema.Query,
    sport_schema.Query,
    event_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    user_schema.Mutation,
    team_schema.Mutation,
    feed_schema.Mutation,
    sport_schema.Mutation,
    event_schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
