from . import types, models
from django.db.models import Q
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required

from users import models as user_models


@login_required
def resolve_get_my_feed(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    user = info.context.user

    posts = user.post.all()
    pg = Paginator(posts, 5)
    if page_num > pg.num_pages:
        return types.GetMyFeedResponse(
            posts=None, page_num=page_num, has_next_page=False
        )

    posts = pg.get_page(page_num)
    if page_num + 1 > pg.num_pages:
        has_next_page = False
    else:
        has_next_page = True
    return types.GetMyFeedResponse(
        posts=posts, page_num=page_num, has_next_page=has_next_page
    )


@login_required
def resolve_get_user_feed(self, info, **kwargs):

    user_id = kwargs.get("user_id")
    page_num = kwargs.get("page_num", 1)

    try:
        user = user_models.User.objects.get(id=user_id)

        posts = user.post.all()
        pg = Paginator(posts, 5)

        if page_num > pg.num_pages:
            return types.GetUserFeedResponse(
                posts=None, page_num=page_num, has_next_page=False
            )

        posts = pg.get_page(page_num)
        if page_num + 1 > pg.num_pages:
            has_next_page = False
        else:
            has_next_page = True
        return types.GetUserFeedResponse(
            posts=posts, page_num=page_num, has_next_page=has_next_page
        )

    except models.Event.DoesNotExist:
        return types.GetUserFeedResponse(posts=None)


@login_required
def resolve_get_main_feed(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    user = info.context.user

    criterion1 = Q(posted_by__in=user.following.all())
    criterion2 = Q(posted_by=user)

    posts = models.Post.objects.filter(criterion1 | criterion2)
    pg = Paginator(posts, 5)

    if page_num > pg.num_pages:
        return types.GetMainFeedResponse(
            posts=None, page_num=page_num, has_next_page=False
        )

    posts = pg.get_page(page_num)
    if page_num + 1 > pg.num_pages:
        has_next_page = False
    else:
        has_next_page = True
    return types.GetMainFeedResponse(
        posts=posts, page_num=page_num, has_next_page=has_next_page
    )
