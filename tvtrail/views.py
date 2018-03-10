from django.shortcuts import render, redirect
from django.http import HttpResponse
from tvtrail.models import tv_show, season, episode, UserProfile
from tvtrail.models import user_episode_relation, user_show_relation
from tvtrail.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your views here.

def index(request):
    context_dict = {'random':"random text"}
    return render(request, 'tvtrail/index.html', context=context_dict)


def about(request):
    context_dict = {'random':"random"}
    return render(request, 'tvtrail/about.html', context=context_dict)

@login_required
def show_tvseries(request, username, tv_show_slug):
    context_dict = {}

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    try:
        show = tv_show.objects.get(show_slug=tv_show_slug)
        seasons = season.objects.filter(show_name=show)
        episodes = episode.objects.filter(show_id=show)
        show_status = user_show_relation.objects.get(user=userprofile ,show=show)
        episode_status = user_episode_relation.objects.filter(user=userprofile, show=show)
        avg_show_rating = user_show_relation.objects.filter(show=show)
        average = 0
        counter = 0
        for status in avg_show_rating:
            counter = counter + 1
            average = average + status.rating
            average = average/counter


        context_dict['show'] = show
        context_dict['seasons'] = seasons
        context_dict['episodes'] = episodes
        context_dict['active_user'] = user
        context_dict['ep_status'] = episode_status
        context_dict['show_status'] = show_status
        context_dict['avg_show_rating'] = avg_show_rating
        context_dict['average'] = average

    except tv_show.DoesNotExist:
        context_dict['show'] = None
        context_dict['seasons'] = None
        context_dict['episodes'] = None
        context_dict['active_user'] = None
        context_dict['ep_status'] = None
        context_dict['show_status'] = None
        context_dict['avg_show_rating'] = None
        context_dict['average'] = None

    return render(request, 'tvtrail/series.html', context_dict)

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)
    context_dict = {'form':form}
    return render(request, 'tvtrail/profile_registration.html', context_dict)

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture, 'watchlist': userprofile.watchlist})

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)
    
    return render(request, 'tvtrail/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})

    