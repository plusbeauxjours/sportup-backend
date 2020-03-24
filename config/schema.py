import graphene
import graphql_jwt

from auth import schema as auth_schema
from profiles import schema as profiles_schema
from teams import schema as teams_schema
from feed import schema as feed_schema
from sports import schema as sports_schema
from events import schema as events_schema


class Query(
    profiles_schema.Query,
    teams_schema.Query,
    feed_schema.Query,
    sports_schema.Query,
    events_schema.Query,
    graphene.ObjectType,
):
    pass


class Mutation(
    auth_schema.Mutation,
    profiles_schema.Mutation,
    teams_schema.Mutation,
    feed_schema.Mutation,
    sports_schema.Mutation,
    events_schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
