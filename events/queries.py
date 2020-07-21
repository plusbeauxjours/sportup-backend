import datetime
from django.db.models import Q
from django.core.paginator import Paginator
from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_event(self, info, **kwargs):
    event_id = kwargs.get("event_id")

    try:
        event = models.Event.objects.get(id=event_id)
        return types.GetEventResponse(event=event)

    except models.Event.DoesNotExist:
        return types.GetEventResponse(event=None)


@login_required
def resolve_get_registrations(self, info, **kwargs):
    event_id = kwargs.get("event_id")

    registrations = models.Registration.objects.filter(event__id=event_id).order_by(
        "approved"
    )
    return types.GetRegistrationsResponse(registrations=registrations)


@login_required
def resolve_get_search_events(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    if search_text == "":
        return types.GetSearchEventsResponse(events=None)
    else:
        events = models.Event.objects.filter(name__icontains=search_text)[:3]
        return types.GetSearchEventsResponse(events=events)


@login_required
def resolve_get_upcoming_events(self, info, **kwargs):

    page_num = kwargs.get("page_num", 1)
    today = datetime.datetime.today()

    events = models.Event.objects.filter(Q(start_date__gte=today) | Q(start_date=None))
    count = events.count()
    pg = Paginator(events, 7)
    if page_num > pg.num_pages:
        return types.GetUpcomingEventsResponse(
            events=None, page_num=page_num, has_next_page=False, count=count
        )

    events = pg.get_page(page_num)
    if page_num + 1 > pg.num_pages:
        has_next_page = False
    else:
        has_next_page = True
    return types.GetUpcomingEventsResponse(
        events=events, page_num=page_num, has_next_page=has_next_page, count=count
    )
