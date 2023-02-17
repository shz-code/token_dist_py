from django.shortcuts import render
from .models import Token, Event, StudentList
from django.http import JsonResponse, HttpResponse
import math
import json
from django.utils.timezone import now
import time

# Create your views here.
def token(request, pk):
    event = Event.objects.get(id=pk)

    end_event = event.event_date
    end_event = int(end_event.strftime('%Y%m%d%H%M'))

    current_date = now()
    current_date = int(current_date.strftime('%Y%m%d%H%M'))

    if current_date > end_event:
        return HttpResponse("This event has already finished. To generate tokens please consider changing event date from event management page. Thanks.")
    context = {
        "event": event,
    }
    return render(request, "tokens.html", context)

def print_token(request, num, pk):
    event = Event.objects.get(id=pk)
    count = event.get_tokens_non_printed_count
    if num > count:
        num = count
    tokens = event.token_set.filter(is_printed=False)[:num]
    token_index = []

    total_pgs = math.ceil(num/10)

    try:
        st = tokens[0].token_serial
        last_ck = tokens[num-1].token_serial
        start_token = tokens[0].token_serial
        end_token = tokens[num-1].token_serial
    except:
        st = 0
        last_ck = 0
        start_token = 0
        end_token = 0

    if total_pgs <= 17:
        meta_pg = 1
    elif total_pgs <= 43:
        meta_pg = 2
    elif total_pgs > 43:
        meta_pg = 3

    for i in range(total_pgs):
        if st + 9 <= last_ck:
            ft = st + 9
        else:
            ft = (last_ck - st) + st
        token_index.append({"page":(i+1+meta_pg),"starting_token":st,"finish_token": ft,"count":(ft-st)+1})
        st = ft + 1
    
    dt = now()

    context = {
        "num": num,
        "event": event,
        "tokens": tokens,
        "start_token": start_token,
        "end_token": end_token,
        "token_index": token_index,
        "total_pgs": total_pgs+meta_pg,
        "dt": dt
    }
    return render(request,"print_tokens.html",context)

def generate_tokens(request):
    if request.method == "POST":
        data = json.loads(request.body)
        num = data['num']
        event_id = data['event_id']
        event = Event.objects.get(id=event_id)

        bulk_list = list()

        num = int(num)
        if num > 300:
            num = 300
        for i in range(num):
            bulk_list.append(
                Token(event=event,usage = event.token_usage)
            )
        Token.objects.bulk_create(bulk_list)
    return JsonResponse({"msg":"Ok"}, safe=False)

def update_print_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        num = data['total_tokens']
        starting_token_id = data['s_token_id']
        ending_token_id = int(starting_token_id) + int(num)
        start = time.time()
        for i in range(int(starting_token_id),ending_token_id):
            token = Token.objects.get(token_serial=i)
            token.is_printed = True
            token.save()
        end = time.time()
        print(end-start)
    return JsonResponse({"msg":"Done"}, safe=False)

def scanner_dist(request, pk):
    event = Event.objects.get(id=pk)
    context = {
        "event": event
    }
    return render(request, "scanner_dist.html",context)

def scanner_receive(request, pk):
    event = Event.objects.get(id=pk)
    context = {
        "event": event
    }
    return render(request, "scanner_receive.html",context)

def token_activate(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data['code']
        stu_id = data['stu_id']
        event_id = data['event_id']

        event = Event.objects.get(id = event_id)
        msg = "404"
        stu = ""
        try:
            stu = StudentList.objects.get(student_id = stu_id,event = event)
            if stu.claimed == True:
                msg = "303"
                return JsonResponse({"msg":msg}, safe=False)
        except:
            msg = "304"
            return JsonResponse({"msg":msg}, safe=False)
        try:
            # token = Token.objects.get(token_serial="1845",event=event,is_printed=True)
            token = Token.objects.get(token_serial=code,event=event,is_printed=True)
            if token.is_activated == True:
                msg = "403"
            else:
                msg = "200"
                token.student_id = stu_id
                token.is_activated = True
                token.save()
                stu.claimed = True
                stu.save()
            return JsonResponse({"msg":msg}, safe=False)
        except:
            return JsonResponse({"msg":msg}, safe=False)
    return JsonResponse({"msg":"No permission"}, safe=False)

def token_activate_new(request):
    if request.method == "POST":
        data = json.loads(request.body)
        event_id = data['event_id']
        code = data['code']
        stu_id = data['stu_id']
        name = data['name']

        event = Event.objects.get(id = event_id)
        msg = "404"
        try:
            # token = Token.objects.get(token_serial="2051",event=event,is_printed=True)
            token = Token.objects.get(token_serial=code,event=event,is_printed=True)
            if token.is_activated == True:
                msg = "403"
            else:
                msg = "200"
                token.student_id = stu_id
                token.is_activated = True
                token.save()
                StudentList.objects.create(
                    name = name,
                    student_id = stu_id,
                    event = event,
                    claimed = True
                )
            return JsonResponse({"msg":msg}, safe=False)
        except:
            return JsonResponse({"msg":msg}, safe=False)
    return JsonResponse({"msg":"No permission"}, safe=False)
            

def token_receive(request):
    if request.method == "POST":
        data = json.loads(request.body)
        code = data['code']
        event_id = data['event_id']
        tag = data['tag']
        msg = "404"
        event = Event.objects.get(id = event_id)
        try:
            # token = Token.objects.get(token_serial=code,event=event,is_printed=True)
            token = Token.objects.get(token_serial="1844",event=event,is_printed=True)
            if token.is_activated == False:
                msg = "403"
                return JsonResponse({"msg":msg}, safe=False)
            else:
                if int(tag) == 2:
                    if token.food_flag == False:
                        msg = "402"
                        return JsonResponse({"msg":msg}, safe=False)
                    else:
                        token.food_flag = False
                        msg = "202"
                        token.save()
                        return JsonResponse({"msg":msg}, safe=False)
                elif int(tag) == 1:
                    if token.entry_flag == False:
                        msg = "401"
                        return JsonResponse({"msg":msg}, safe=False)
                    else:
                        token.entry_flag = False
                        msg = "201"
                        token.save()
                        return JsonResponse({"msg":msg}, safe=False)
        except:
            return JsonResponse({"msg":msg}, safe=False)
    return JsonResponse({"msg":"No premission"}, safe=False)