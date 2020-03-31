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


def resolve_get_registrations(self, info, **kwargs):
    event_id = kwargs.get("event_id")

    try:
        registration = models.Registration.objects.filter(event__pk=event_id).order_by(
            "approved"
        )
        return types.GetRegistrationResponse(registration=registration)

    except models.Registration.DoesNotExist:
        return types.GetRegistrationResponse(registration=None)
