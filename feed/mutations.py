import graphene
from . import types, models
from graphql_jwt.decorators import login_required


class PostMutation(graphene.Mutation):

    Output = types.PostMutationReponse

    def mutate(self, info, **kwargs):
        return types.PostMutationReponse(ok=True)


class CreatePost(graphene.Mutation):
    class Arguments:
        text = graphene.String(required=True)

    Output = types.CreatePostReponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        text = kwargs.get("text")

        post = models.Post.objects.create(posted_by=user, text=text)

        return types.CreatePostReponse(post=post)
