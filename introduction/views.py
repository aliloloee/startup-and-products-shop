from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache.utils import make_template_fragment_key as mtfk
from django.utils.translation import get_language
from django.conf import settings

from .models import Service, Benefit, TeamMember, Contact, Banner
from .forms import ContactForm
from BANPars.redis_conf import redis

import json


def intro(request) :
    
    prefix=settings.CACHES['default']['KEY_PREFIX']
    db_number = settings.CACHE_DB_NUMBER

    context = {}
    lang = get_language()
    model_list = [Service, Benefit, TeamMember, Banner]

    for model in model_list :

        base_key =  mtfk(f'{model.__name__.lower()}', [lang, ])
        key = f'{prefix}:{db_number}:{base_key}'

        if not redis.exists(key) :
            context[f'{model.__name__.lower()}s'] = model.objects.all()


    return render(request, 'introduction/company.html', context)




def contact(request) :
    if request.method == 'GET' :
        initial = {}
        try :
            fullname = request.user.fullname
        except :
            fullname = None
        initial['fullname'] = fullname
        form = ContactForm(initial=initial)

    if request.is_ajax() and request.method == 'POST' :
        body = json.loads(request.body.decode("utf-8"))
        try :
            if request.user.is_authenticated :
                body['mobile'] = request.user.username
            Contact.objects.create(**body)
        except Exception as e:
            return JsonResponse({'body' : f'{e}'}, status=400)

        return JsonResponse({'body' : 'message sent successfully'}, status=201)

    context = {
        'form' : form,
    }
    return render(request, 'introduction/contact.html', context)
