from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from WebNotifier.models import *


def page_list(request):
    result = ''
    if request.method == 'POST':
        try:
            device_id = request.POST['device_id']
            device = Device.objects.get(id=device_id)
            pages = Page.objects.filter(user_profile=device.user, active=True)
            result = ', '.join('{' + ', '.join(['"id": ' + str(page.id),
                                                '"url": "' + page.page_url + '"',
                                                '"paths": ' + page.page_data,
                                                '"interval": ' + str(page.interval),
                                                '"login_url": "' + page.login_url + '"',
                                                '"login_data": ' + page.login_data]) + '}' for page in pages)
        except (KeyError, ObjectDoesNotExist):
            pass
    return HttpResponse('[' + result + ']')


def new_change(request):
    if request.method == 'POST':
        pass