from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from WebNotifier.models import *
import json


def page_list(request):
    result = ''
    try:
        device = Device.objects.get(id=request.POST['device_id'])
        pages = Page.objects.filter(user_profile=device.user, active=True)
        result = ', '.join('{' + ', '.join(['"id": ' + str(page.id),
                                            '"url": "' + page.page_url + '"',
                                            '"paths": ' + page.page_data,
                                            '"interval": ' + str(page.interval),
                                            '"login_url": "' + page.login_url + '"',
                                            '"login_data": ' + page.login_data]) + '}' for page in pages)
    except KeyError:
        return HttpResponse('Missing POST data.', status=400)
    except ObjectDoesNotExist:
        return HttpResponse('Invalid device id.', status=401)

    return HttpResponse('[' + result + ']')


def new_change(request):
    try:
        device = Device.objects.get(id=request.POST['device_id'])
        page = Page.objects.get(id=request.POST['page_id'], user_profile=device.user)
        old_value = request.POST['old_value']
        new_value = request.POST['new_value']
        change = Change(page=page, date=timezone.now(), old_value=old_value, new_value=new_value)
        change.save()
    except KeyError:
        return HttpResponse('Missing POST data.', status=400)
    except ObjectDoesNotExist:
        return HttpResponse('Invalid device or page id.', status=401)

    return HttpResponse('')


def what(request):
    try:
        device = Device.objects.get(id=request.POST['device_id'])
        msg = request.POST['msg']
    except KeyError:
        return HttpResponse('Missing POST data.', status=400)
    except ObjectDoesNotExist:
        return HttpResponse('Invalid device.', status=401)

    that = 'nothing'

    if msg == 'hi':
        that = 'hello'
    elif msg == 'bye':
        that = 'see you soon!'
    elif msg == 'what':
        that = 'that'

    ret = {'that': that}
    return HttpResponse(json.dumps(ret))
