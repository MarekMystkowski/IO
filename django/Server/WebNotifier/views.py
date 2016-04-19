from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from WebNotifier.models import UserProfile, Page
import urllib.parse


@login_required
def add(request):
    if request.method != 'POST':
        raise Http404("No POST data found.")
    try:
        page_url = request.POST['page_url']
        page_data = request.POST['page_data']
        login_url = request.POST['login_url']
        login_data = request.POST['login_data']
    except KeyError:
        raise Http404("Not enough POST data found.")

    user_profile = UserProfile.objects.get(user=request.user)
    page = Page(user_profile=user_profile, page_url=page_url, page_data=page_data, login_url=login_url, login_data=login_data)



    page.save()

    request.session['page_id'] = page.id

    return render(request, 'edit_page.html', {
        'page_url': page_url,
        'interval': '.'.join(str(page.interval).split(',')),
        'active': True,
    })

@login_required
def edit_page(request):
    try:
        page_id = request.session['page_id']
        page = Page.objects.get(id=page_id)
    except KeyError:
        return HttpResponseRedirect('/')

    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile != page.user_profile:
        HttpResponseRedirect('/')

    if request.method == 'POST':
        try:
            page.interval = int(float(request.POST['interval']))
            page.active = False
            if request.POST['active'] == 'True':
                page.active = True
        except KeyError:
            pass

    page.save()

    return render( request, 'edit_page.html', {
        'page_url': page.page_url,
        'interval': '.'.join(str(page.interval).split(',')),
        'active': page.active,
    })