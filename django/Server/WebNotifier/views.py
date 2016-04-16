from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required
from WebNotifier.models import UserProfile, PageToObserve
from datetime import timedelta
import urllib.parse

@login_required
def add(request):
    if request.method != 'POST':
        raise Http404("Nie ma danych POST")

    try:
        data_from_plugin_string = request.POST['choice']
    except (KeyError):
        raise Http404("Nie ma właściwych danych POST")

    user_profile = UserProfile.objects.filter(user=request.user)

    # załądowanie danych z wtyczki
    def is_path(tuple):
        try:
            x = len(tuple)
            for z in tuple:
                z = z + 1
                if z < 1: raise
        except:
            return False;
        return True

    # Załadowanie danych i sprawdzenie ich poprawności, w razie błędu zwraca 404 i odpowiendni komunikaty wypisuje.
    try:
        plugin = {}
        url_login = ""
        login_data = ""
        exec("data = " + data_from_plugin_string) in plugin
        inputs = plugin["data"]["inputs"]
        submit= plugin["data"]["inputs"]
        objects = plugin["data"]["object"]

        if(len(inputs) != 0):
            if(inputs[0]['url'] != submit['url']):
                print('Adres do zalogowania inny niż w polach do logowania. Nie spójne dane.')
                raise
            tmp = urllib.parse.urlsplit(submit['url'])
            url_login = submit['url']

            if is_path(tuple=submit['path']):
                print('W submit ścieżka nie spełnia standardu.')
                raise

            for x in inputs[1:]:
                if is_path(tuple=x['path']):
                    print('W inputs ścieżka nie spełnia standardu.')
                    raise
                tmp = x['value'] + " "

            login_data = "{ 'inputs' : " + str(inputs) + " 'submit' : " + str(submit['path']) + " }"

        for x in objects:
            if is_path(tuple=x['path']):
                print('W inputs ścieżka nie spełnia standardu.')
                raise
            tmp = urllib.parse.urlsplit(x['url'])
        url_base = urllib.parse.urlsplit(objects[0]['url']).geturl()
        if len(url_base) > 50: url_base = url_base[0:46] + " ..."

        data_to_observer = str(object)
    except:
        print("Dane z wtyczki które spowodowały błąd:", data_from_plugin_string)
        raise Http404("Dane ze wtyczki nie poprawne")

    new_page = PageToObserve(url_to_login=url_login, login_data=login_data, data_to_observer=data_to_observer,
                             user=user_profile, last_page_content = "", refresh_period = timedelta(seconds=15))
    new_page.save()



    return render( request, 'add.html', {
        'name_url' : url_base,
        'refresh_period' : new_page.refresh_period,
    })
