from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from users.models import EventPermission
from tokens.models import Event, Tag, Token
from users.models import User
from django.utils.timezone import now
import json
from django.conf import settings
import time

# Create your views here.

def index(request):
    return HttpResponse("Index")

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
        pk = request.POST.get('pk')
        name = request.POST.get('name')
        place = request.POST.get('place')
        date = request.POST.get('date')
        time = request.POST.get('time')
        token_start_date = request.POST.get('token_start_date')
        token_start_time = request.POST.get('token_start_time')
        token_end_date = request.POST.get('token_end_date')
        token_end_time = request.POST.get('token_end_time')
        desc = request.POST.get('desc')
        usage = request.POST.get('usage')
        
        time = date+" "+time+":00.000000"
        token_start_time = token_start_date+" "+token_start_time+":00.000000"
        token_end_time = token_end_date+" "+token_end_time+":00.000000"

        event = Event.objects.get(id = pk)
        tags_count = Tag.objects.all().count()

        
        if int(usage) <= tags_count:
            if int(usage) != int(event.token_usage):
                Token.objects.filter(event=event, usage = event.token_usage).delete()
                event.token_usage = usage

        tags = request.POST.getlist('tags')
        if tags != 'None':    
            if len(tags) == int(event.token_usage):
                event.tags.clear()
                for tag in tags:
                    event.tags.add(tag)

        executives = request.POST.getlist('users')
        if executives != 'None':    
            EventPermission.objects.filter(event=event).delete()
            for executive in executives:
                user = User.objects.get(id=executive)
                EventPermission.objects.create(
                    event = event,
                    user = user
                )

        event.name = name
        event.distribution_place = place
        event.event_date = time
        event.token_dist_start = token_start_time
        event.desc = desc

        event.save()

    return redirect(f'/event/{pk}')

def delete_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id = data['event_id']
        # Event.objects.get(id=id).delete()
    return JsonResponse({"msg":"Deleted"},safe=False)