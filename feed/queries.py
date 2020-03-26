from . import types
from django.core.paginator import Paginator
from graphql_jwt.decorators import login_required


@login_required
def resolve_my_feed(self, info, page_num=1):
    user = info.context.user
    uf = user.post.all()
    pg = Paginator(uf, 7)

    if page_num > pg.num_pages:
        return None

    feeds = pg.get_page(page_num)
    return types.MyFeedResponse(feeds=feeds)
