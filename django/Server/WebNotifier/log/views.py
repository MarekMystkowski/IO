from WebNotifier.log.forms import UserForm
from WebNotifier.models import UserProfile
from django.template import RequestContext
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            UserProfile(user = user, account_type = '5', date_of_registration = timezone.now()).save()

            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render( request, 'registration/register.html', {
        'user_form': user_form,
        'registered': registered
    })

def user_login(request):
    try:
        next_page = request.POST['next']
    except:
        next_page = "/"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid log details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid log details supplied.Erro")

    else:
        return render(request, 'registration/login.html', {'next': request.GET['next'] if request.GET and 'next' in request.GET else ''})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/log/')

def index(request):
    context = RequestContext(request)
    return render_to_response('registration/index.html', {}, context)