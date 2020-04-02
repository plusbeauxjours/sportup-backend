import datetime
from django.db.models import Q
from . import types, models
from graphql_jwt.decorators import login_required


@login_required
def resolve_get_event(self, info, **kwargs):
    event_id = kwargs.get("event_id")

    try:
        event = models.Event.objects.get(pk=event_id)
        return types.GetEventResponse(event=event)

    except models.Event.DoesNotExist:
        return types.GetEventResponse(event=None)


def resolve_get_registration(self, info, **kwargs):
    event_id = kwargs.get("event_id")

    registration = models.Registration.objects.filter(event__pk=event_id).order_by(
        "approved"
    )
    return types.GetRegistrationResponse(registration=registration)


def resolve_get_search_events(self, info, **kwargs):
    search_text = kwargs.get("search_text", "")

    events = models.Event.objects.filter(name__icontains=search_text)[:3]
    return types.GetSearchEventsResponse(events=events)


def resolve_get_upcoming_events(self, info):
    today = datetime.datetime.today()

    events = models.Event.objects.filter(Q(start_date__gte=today) | Q(start_date=None))
    return types.GetUpcomingEventsResponse(events=events)
