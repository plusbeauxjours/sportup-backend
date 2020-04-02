import graphene
from . import types, models
from graphql_jwt.decorators import login_required


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


class UpvotePost(graphene.Mutation):
    class Arguments:
        postId = graphene.Int()

    Output = types.UpvotePostResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        postId = kwargs.get("postId")

        try:
            post = models.Post.objects.get(pk=postId)

            try:
                upi = models.UserPostInteraction.objects.get(user=user, post=post)

                if upi.interaction == "UV":
                    return types.UpvotePostResponse(ok=True)
                if upi.interaction == "DV":
                    post.score += 1

                upi.interaction = "UV"
                upi.save()

            except models.UserPostInteraction.DoesNotExist:
                models.UserPostInteraction.objects.create(
                    user=user, post=post, interaction="UV"
                )

            post.score += 1
            post.save()

            return types.UpvotePostResponse(ok=True)

        except models.Post.DoesNotExist:
            return types.UpvotePostResponse(ok=False)


class DownvotePost(graphene.Mutation):
    class Arguments:
        postId = graphene.Int()

    Output = types.DownvotePostResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        postId = kwargs.get("postId")

        try:
            post = models.Post.objects.get(pk=postId)

            try:
                upi = models.UserPostInteraction.objects.get(user=user, post=post)

                if upi.interaction == "DV":
                    return types.DownvotePostResponse(ok=True)
                if upi.interaction == "UV":
                    post.score -= 1

                upi.interaction = "DV"
                upi.save()

            except models.UserPostInteraction.DoesNotExist:
                models.UserPostInteraction.objects.create(
                    user=user, post=post, interaction="DV"
                )

            post.score -= 1
            post.save()

            return types.DownvotePostResponse(ok=True)

        except models.Post.DoesNotExist:
            return types.UpvotePostResponse(ok=False)


class RemovePostInteraction(graphene.Mutation):
    class Arguments:
        postId = graphene.Int()

    Output = types.RemovePostInteractionResponse

    @login_required
    def mutate(self, info, **kwargs):
        user = info.context.user
        postId = kwargs.get("postId")

        try:
            post = models.Post.objects.get(pk=postId)

            try:
                upi = models.UserPostInteraction.objects.get(user=user, post=post)
                if upi.interaction == "UV":
                    post.score -= 1
                elif upi.interaction == "DV":
                    post.score += 1
                upi.delete()
                post.save()
            except models.UserPostInteraction.DoesNotExist:
                pass

            return types.RemovePostInteractionResponse(ok=True)

        except models.Post.DoesNotExist:
            return types.UpvotePostResponse(ok=False)
