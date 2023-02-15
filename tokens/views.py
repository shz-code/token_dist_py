from django.shortcuts import render
from .models import Token, Event
from django.http import HttpResponse
import math
from django.utils.timezone import now

# Create your views here.
def token(request, pk):
    event = Event.objects.get(id=pk)
    context = {
        "event": event,
    }
    return render(request, "tokens.html", context)

def scanner(request):
    return render(request, "scanner.html")

def print_token(request, num, pk):
    event = Event.objects.get(id=pk)
    count = event.get_tokens_non_printed_count
    if num > count:
        num = count
    pg = 0
    tokens = event.token_set.filter(is_printed=False)[:num]
    token_index = []

    total_pgs = math.ceil(num/10)


    st = tokens[0].token_serial
    last_ck = tokens[num-1].token_serial

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
        "start_token": tokens[0],
        "end_token": tokens[num-1],
        "token_index": token_index,
        "total_pgs": total_pgs,
        "dt": dt
    }
    return render(request,"print_tokens.html",context)