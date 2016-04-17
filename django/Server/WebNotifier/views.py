from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from WebNotifier.models import UserProfile, PageToObserve
import urllib.parse


def url_name(url):
    url_base = urllib.parse.urlsplit(url).geturl()
    if len(url_base) > 50: url_base = url_base[0:46] + " ..."
    return url_base

@login_required
def add(request):
    if request.method != 'POST':
        raise Http404("Nie ma danych POST")

    try:
        url_login = request.POST['url_login']
        login_data = request.POST['login_data']
        data_to_observer = request.POST['data_to_observer']
    except (KeyError):
        raise Http404("Nie ma właściwych danych POST")

    user_profile = UserProfile.objects.filter(user=request.user).first()

    new_page = PageToObserve(url_to_login=url_login, login_data=login_data, data_to_observer=data_to_observer,
                             user=user_profile)
    new_page.save()

    request.session['id_page'] = new_page.id

    return render( request, 'edit_page.html', {
        'name_url' : url_name(url_login),
        'refresh_period' : '.'.join(str(new_page.refresh_period_ms / 1000).split(',')),
        'currently_observed' : True,
    })

@login_required
def edit_page(request):
    try:
        id_page =  request.session['id_page']
        page = PageToObserve.objects.filter(id=id_page).first()
    except KeyError:
        return HttpResponseRedirect('/')
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if user_profile != page.user :
        HttpResponseRedirect('/')


    if request.method == 'POST':
        try:
            page.refresh_period_ms = int(float(request.POST['period']) * 1000)
            page.currently_observed = False
            if request.POST['currently'] == 'True': page.currently_observed = True
        except KeyError: pass

    page.save()

    return render( request, 'edit_page.html', {
        'name_url' : url_name(page.url_to_login),
        'refresh_period' : '.'.join(str(page.refresh_period_ms / 1000).split(',')),
        'currently_observed' : page.currently_observed,
    })