from . import types, models
from django.db.models import Q
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from users import models as user_models


@login_required
def resolve_my_feed(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    user = info.context.user

    posts = user.post.all()
    pg = Paginator(posts, 2)
    if page_num > pg.num_pages:
        return None
    print("page_num", page_num, "pg.num_pages", pg.num_pages)

    posts = pg.get_page(page_num)
    return types.MyFeedResponse(posts=posts)


@login_required
def resolve_user_feed(self, info, **kwargs):

    uuid = kwargs.get("uuid")
    page_num = kwargs.get("page_num", 1)

    try:
        user = user_models.User.objects.get(uuid=uuid)

        posts = user.post.all()
        pg = Paginator(posts, 2)

        if page_num > pg.num_pages:
            return None

        posts = pg.get_page(page_num)
        return types.UserFeedResponse(posts=posts)

    except models.Event.DoesNotExist:
        return types.UserFeedResponse(posts=None)


@login_required
def resolve_main_feed(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    user = info.context.user

    criterion1 = Q(posted_by__in=user.following.all())
    criterion2 = Q(posted_by=user)

    posts = models.Post.objects.filter(criterion1 | criterion2)
    pg = Paginator(posts, 2)

    if page_num > pg.num_pages:
        return None

    posts = pg.get_page(page_num)
    return types.MainFeedResponse(posts=posts)
