from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from push_notifications.models import GCMDevice

from WebNotifier.models import UserProfile, Page, Device, Change


def update_device(user):
    if user.active_device != '':
        active_dev = Device.objects.get(id=user.active_device)
        if active_dev.buffer == '':
            active_dev.buffer = 'update'
        active_dev.save()

def priorities_changed(user_profile):
    # TODO to samo co w api/views.py
    active_devs = Device.objects.filter(user=user_profile, active=True).order_by('priority')
    if len(active_devs) > 0:
        topd = active_devs[0]
        if user_profile.active_device != topd.id:
            ad = Device.objects.get(id=user_profile.active_device)
            ad.buffer = 'stop'
            ad.save()
            user_profile.active_device = topd.id
            user_profile.save()


def add_page(request):
    try:
        request.session['new_page'] = True
        for name in ['page_url', 'page_title', 'page_data', 'login_url','login_data']:
            request.session[name] = request.POST[name]
    except:
        request.session['new_page'] = False
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/edit_page')


@login_required
def edit_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.session['new_page']:
        request.session['new_page'] = False
        page_url = request.session['page_url']
        page_title = request.session['page_title']
        page_data = request.session['page_data']
        login_url = request.session['login_url']
        login_data = request.session['login_data']
        # dodajemy stronę, ale aktywować możemy dopiero po kliknięciu "zapisz"
        # chodzi o to żeby odświeżaczka pobrała stronę dopiero gdy ustawimy częstotliwość
        page = Page(user_profile=user_profile, page_url=page_url, title=page_title, page_data=page_data, login_url=login_url, login_data=login_data, active=False)
        page.save()

        return render(request, 'edit_page.html', {
            'page': page,
            'active': True
        })

    if request.method == 'POST':
        try:
            page = Page.objects.get(id=request.POST['page_id'])
            page.title = request.POST['title']
            page.interval = request.POST['interval']
            page.active = False
            if request.POST.get('active', False):
                page.active = True
            page.save()
            update_device(user_profile)
        except KeyError:
            pass

    return HttpResponseRedirect('/')


@login_required
def index(request):
    max_quantity = 20
    user_profile = UserProfile.objects.get(user=request.user)
    pages = Page.objects.all().filter(user_profile=user_profile).order_by('-id')
    devices = Device.objects.all().filter(user=user_profile).order_by('priority')

    # Akcje:
    if request.method == 'POST':
        if request.POST.get('submit_sav_page', False):
            page_id = request.POST['page_id']
            page = Page.objects.get(id=page_id)
            page.active = request.POST.get('active', "") == "True"
            page.interval = request.POST['interval']
            page.save()
            update_device(user_profile)
        if request.POST.get('submit_del_page', False):
            page_id = request.POST['page_id']
            page = Page.objects.get(id=page_id)
            page.delete()
            update_device(user_profile)
        if request.POST.get('submit_up_device', False):
            device_id = request.POST['device_id']
            device1 = Device.objects.get(id=device_id)
            device2 = Device.objects.get(priority=(device1.priority - 1))
            device1.priority -= 1
            device2.priority += 1
            device1.save()
            device2.save()
            priorities_changed(user_profile)
        if request.POST.get('submit_down_device', False):
            device_id = request.POST['device_id']
            device1 = Device.objects.get(id=device_id)
            device2 = Device.objects.get(priority=(device1.priority + 1))
            device1.priority += 1
            device2.priority -= 1
            device1.save()
            device2.save()
            priorities_changed(user_profile)
        #TODO, ale nie trzeba tego prezentować
        if request.POST.get('submit_del_device', False):
            device_id = request.POST['device_id']
            device = Device.objects.get(id=device_id)
            for dev in Device.objects.all().filter(priority__gt=device.priority):
                dev.priority -= 1
                dev.save()
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

    new_changes = []
    old_changes = []
    for page in pages:
        new_changes.extend(Change.objects.all().filter(page=page, displayed=False))
        old_changes.extend(Change.objects.all().filter(page=page, displayed=True).order_by('-date')[:max_quantity])
        new_changes.sort(key=lambda x: x.date, reverse=True)
        old_changes = sorted(old_changes, key=lambda x: x.date)[::-1][:max_quantity]

    return render(request, 'index.html', {
        'pages' : pages,
        'devices': devices,
        'len_devices': len(devices),
        'new_changes' : new_changes,
        'old_changes' : old_changes,
    })


def add_device(request):
    try:
        request.session['new_device'] = True
        for name in ['device_id', 'device_name']:
            request.session[name] = request.GET[name]
    except:
        request.session['new_device'] = False
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/edit_device')

@login_required
def edit_device(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.session['new_device']:
        request.session['new_device'] = False
        device_id = request.session['device_id']
        device_name = request.session['device_name']
        if device_id == "":
            return HttpResponseRedirect('/')
        return render(request, 'edit_device.html', {'device_id': device_id, 'device_name': device_name})

    if request.method == 'POST':
        device_id = request.POST.get('device_id', '')
        if device_id == "":
            return HttpResponseRedirect('/')
        name = request.POST.get('name', 'New Device')
        prio = len(Device.objects.filter(user=user_profile)) + 1
        Device(id=device_id, name=name, priority=prio, user=user_profile).save()
        priorities_changed(user_profile)

        return HttpResponseRedirect('/')

    return HttpResponseRedirect('/')


def notify_me(request):
    try:
        request.session['notify_me'] = True
        request.session['rid'] = request.GET['rid']
    except:
        request.session['notify_me'] = False
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/edit_notify')


@login_required
def edit_notify(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.session['notify_me']:
        request.session['notify_me'] = False
        rid = request.session['rid']
        if rid == "":
            return HttpResponseRedirect('/')
        new_notifier = GCMDevice(registration_id=rid, user=user_profile.user)
        new_notifier.save()

    return HttpResponseRedirect('/')