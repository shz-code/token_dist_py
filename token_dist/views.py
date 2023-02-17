from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from users.models import EventPermission
from tokens.models import Event, Token, StudentList
from users.models import User
from django.utils.timezone import now
import json
from django.conf import settings
import time
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from tablib import Dataset

# Create your views here.

def index(request):
    return render(request, "index.html")

def events(request):
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
    return render(request, "events.html", context)

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
            # tags = Tag.objects.all()
            users = User.objects.all().exclude(is_admin=True)
            epall = EventPermission.objects.filter(event=event)
            stu_list = StudentList.objects.filter(event = event).count()
            # context["tags"] = tags
            context["users"] = users
            context["epall"] = epall
            context["stu_list"] = stu_list
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

def event_stulist(request, pk):
    event = Event.objects.get(id = pk)
    stu_list = StudentList.objects.filter(event = event).count()
    status = False
    msg = ""
    type = ""
    context = {
        "event":event,
        "stu_list":stu_list,
    }
    
    if request.method == "POST":
        event = Event.objects.get(id = pk)
        dataset = Dataset()
        new_record = request.FILES.get("student_list")
   
        if not new_record.name.endswith('xlsx'):
            status = True
            msg = "Wrong file format."
            type = "danger"
            context["status"] = status
            context["msg"] = msg
            context["type"] = type
            return render(request, "event_studentlist.html",context)
        
        data = dataset.load(new_record.read(),format="xlsx")
        bulk_list = list()
        for datum in data:
            bulk_list.append(
                StudentList(student_id=datum[1],name = datum[2],event = event)
            )
        StudentList.objects.bulk_create(bulk_list)
    return render(request, "event_studentlist.html",context)

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
        
        if int(usage) != int(event.token_usage):
            if int(usage) > 1:
                Token.objects.filter(event=event).update(
                    entry_flag = True,
                    food_flag = True
                )
                event.token_usage = usage
            elif int(usage) == 1:
                Token.objects.filter(event=event).update(
                    entry_flag = False,
                    food_flag = True
                )
            event.token_usage = usage

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


def create_user(request):
    return render(request, "create_user.html")

def create_user_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data['name']
        username = data['username']
        phone = data['phone']
        email = data['email']
        password = data['password']
        adm = data['adm']
        if adm:
            User.objects.create(
                name = name,
                phone = phone,
                username = username,
                email = email,
                password = make_password(password),
                is_admin = True,
                is_executive = False
            )
        else:
            User.objects.create(
                name = name,
                phone = phone,
                username = username,
                email = email,
                password = make_password(password),
            )
    return JsonResponse({"msg":"Done"},safe=False)


def handle_page_not_found(request, exception):
    return render(request, "404.html")
