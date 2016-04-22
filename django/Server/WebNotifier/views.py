from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from WebNotifier.models import UserProfile, Page, Device, Change
import urllib.parse

@login_required
def add_device(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        device_id = request.POST.get('device_id', "")
        if device_id == "":
            return HttpResponseRedirect('/')
        if request.POST.get('of_page', False):
            name = request.POST.get('name', "")
            prio = len(Device.objects.all().filter(user_profile=user_profile)) + 1
            Device(id=device_id, name=name, priority=prio, user=user_profile).save()
            return HttpResponseRedirect('/')
        else:
            return render( request, 'add_device.html', {'device_id': device_id})
    return HttpResponseRedirect('/')

@login_required
def add_page(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.POST.get('of_page', False):
            try:
                page = Page.objects.get(id=request.POST['page_id'])
                page.interval = int(float(request.POST['interval']))
                page.active = False
                if request.POST['active'] == 'True':
                    page.active = True
                page.save()
            except KeyError: pass
            return HttpResponseRedirect('/')
        else:
            try:
                page_url = request.POST['page_url']
                page_data = request.POST['page_data']
                login_url = request.POST['login_url']
                login_data = request.POST['login_data']
            except KeyError:
                raise Http404("Not enough POST data found.")
            page = Page(user_profile=user_profile, page_url=page_url, page_data=page_data, login_url=login_url, login_data=login_data)
            page.save()

            return render(request, 'add_page.html', {
                'page_url': page_url,
                'interval': '.'.join(str(page.interval).split(',')),
                'active': True,
                'page_id' : page.id
            })
    return HttpResponseRedirect('/')

@login_required
def index(request):
    max_quantity = 20
    user_profile = UserProfile.objects.get(user=request.user)
    pages = Page.objects.all().filter(user_profile=user_profile)
    devices = Device.objects.all().filter(user=user_profile)


    # Akcje:
    if request.method == 'POST':
        if request.POST.get('submit_sav_page', False):
            page_id = request.POST['page_id']
            page = Page.objects.get(id=page_id)
            page.active = request.POST.get('active', "") == "True"
            page.interval = request.POST['interval']
            page.save()
        if request.POST.get('submit_del_page', False):
            page_id = request.POST['page_id']
            page = Page.objects.get(id=page_id)
            page.delete()
        if request.POST.get('submit_up_device', False):
            device_id = request.POST['device_id']
            device1 = Device.objects.get(id=device_id)
            device2 = Device.objects.get()

        if request.POST.get('submit_down_device', False):
            device_id = request.POST['device_id']

        if request.POST.get('submit_del_device', False):
            device_id = request.POST['device_id']
            device = Device.objects.get(id=device_id)
            device.delete()
        if request.POST.get('submit_vis_change', False):
            change = Change.objects.get(id=request.POST['change_id'])
            change.displayed = True
            change.save()
        if request.POST.get('submit_vis_all_change', False):
            for page in pages:
                for change in Change.objects.all().filter(page=page, displayed=False):
                    change.displayed = True
                    change.save()

    not_shown_change = []
    shown_change = []
    for page in pages:
        not_shown_change.extend(Change.objects.all().filter(page=page, displayed=False))
        shown_change.extend(Change.objects.all().filter(page=page, displayed=True).order_by('-date')[:max_quantity])
        not_shown_change.sort(key=lambda x: x.date, reverse=True)
        shown_change = sorted(shown_change, key=lambda x: x.date)[::-1][:max_quantity]

    return  render(request, 'index.html', {
        'pages' : pages,
        'is_pages' : len(pages) != 0,
        'devices_and_iter' : map(lambda x,i :(x,i+1), devices, range(len(devices))),
        'len_devices' : len(devices),
        'not_shown_change' : not_shown_change,
        'is_not_shown_change' : len(not_shown_change) != 0,
        'shown_change' : shown_change,
        'is_shown_change' : len(shown_change) != 0
    })


@login_required
def add_device(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        device_id = request.POST.get('device_id', "")
        if device_id == "":
            return HttpResponseRedirect('/')
        if request.POST.get('of_page', False):
            name = request.POST.get('name', "")
            prio = len(Device.objects.all().filter(user_profile=user_profile)) + 1
            Device(id=device_id, name=name, priority=prio, user=user_profile).save()
            return HttpResponseRedirect('/')
        else:
            return render( request, 'add_device.html', {'device_id': device_id})
    return HttpResponseRedirect('/')