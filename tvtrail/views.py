from django.shortcuts import render
from django.http import HttpResponse
from tvtrail.models import tv_show, season, episode
from tvtrail.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    context_dict = {'random':"random text"}
    return render(request, 'tvtrail/index.html', context=context_dict)


def about(request):
    context_dict = {'random':"random"}
    return render(request, 'tvtrail/about.html', context=context_dict)

def show_tvseries(request, tv_show_slug):
    context_dict = {}

    try:
        show = tv_show.objects.get(show_slug=tv_show_slug)
        seasons = season.objects.filter(show_name=show)
        episodes = episode.objects.filter(show_id=show)

        context_dict['show'] = show
        context_dict['seasons'] = seasons
        context_dict['episodes'] = episodes

    except tv_show.DoesNotExist:
        context_dict['show'] = None
        context_dict['seasons'] = None
        context_dict['episodes'] = None

    return render(request, 'tvtrail/series.html', context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'tvtrail/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your TV Trail account is disabled.")
        else: 
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'tvtrail/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

    