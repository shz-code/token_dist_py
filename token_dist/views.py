from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from users.models import EventPermission
from tokens.models import Event, Tag
from users.models import User
from django.utils.timezone import now
import json
from django.conf import settings
# Create your views here.

def dashboard(request):
    events = Event.objects.all()
    up_events = []
    prev_events = []
    for event in events:
        end_date = event.event_date
        current_date = now()
        end_date = int(end_date.strftime('%Y%m%d%H%M'))
        current_date = int(current_date.strftime('%Y%m%d%H%M'))
        if end_date - current_date > 0:
            up_events.append(event)
        else:
            prev_events.append(event)
    context = {
        'up_events': up_events,
        'prev_events': prev_events
    }
    return render(request, "index.html", context)

def event(request, pk):
    user = request.user
    event = Event.objects.get(id=pk)
    token_status = "Token distribution has not started yet. Stay Tuned"

    current_date = now()
    current_date = int(current_date.strftime('%Y%m%d%H%M'))
    
    end_event = event.event_date
    end_event = int(end_event.strftime('%Y%m%d%H%M'))
    if current_date > end_event:
        token_status = "Event Finished. Thanks for your co-operation"
    else:
        try:
            start_date = event.token_dist_start
            end_date = event.token_dist_end
            place = event.distribution_place

            start_date = int(start_date.strftime('%Y%m%d%H%M'))
            end_date = int(end_date.strftime('%Y%m%d%H%M'))
            

            if current_date >= start_date and current_date <= end_date:
                token_status = "Token distribution started. Collect the token from " + place
            elif current_date < start_date:
                pass
            elif current_date > end_date:
                token_status = "Token distribution finished. Enjoy the event"
        except:
            pass
    # Common context
    context = {
            "event": event,
            "token_status": token_status
        }
    
    if user.is_authenticated:
        if user.is_admin:
            tags = Tag.objects.all()
            users = User.objects.all().exclude(is_admin=True)
            epall = EventPermission.objects.filter(event=event)
            context["tags"] = tags
            context["users"] = users
            context["epall"] = epall
            return render(request, "event_admin.html", context)
        else:
            try:
                ep = EventPermission.objects.get(user=user,event=event)
                epall = EventPermission.objects.filter(event=event).exclude(user=user)
                context["user"] = user
                context["epall"] = epall
            except:
                return render(request, "event.html", context)
            return render(request, "event_executive.html", context)
    else:
        return render(request, "event.html", context)
    

def event_update(request):
    if request.method == "POST":
        data = json.loads(request.body)
        date = data['date']
        time = data['time']
        time = date+" "+time+":00.000000"
        event = Event.objects.get(id=1)
        event.event_date = time
        event.save()
    return JsonResponse({'msg': "HI"}, safe=False)