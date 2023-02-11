from django.shortcuts import render, redirect, HttpResponse
from users.models import User
from tokens.models import Event
from django.utils.timezone import now
from datetime import datetime
# Create your views here.

def dashboard(request):
    events = Event.objects.all()
    up_events = []
    prev_events = []
    for event in events:
        end_date = event.event_date
        current_date = now()
        end_date = int(end_date.strftime('%Y%m%d'))
        current_date = int(current_date.strftime('%Y%m%d'))
        if end_date - current_date > 0:
            up_events.append(event)
        else:
            prev_events.append(event)
    context = {
        'up_events': up_events,
        'prev_events': prev_events
    }
    return render(request, "index.html", context)