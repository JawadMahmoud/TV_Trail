from django.shortcuts import render, redirect
from django.http import HttpResponse
from tvtrail.models import tv_show, season, episode, UserProfile, genre
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
def show_tvseries(request, tv_show_slug):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

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

    try:
        show_status = user_show_relation.objects.get(user=userprofile ,show=show)
        context_dict['show_status'] = show_status
    except user_show_relation.DoesNotExist:
        context_dict['show_status'] = None
        
    try:
        episode_status = user_episode_relation.objects.filter(user=userprofile, show=show)
        context_dict['ep_status'] = episode_status
    except user_episode_relation.DoesNotExist:
        context_dict['ep_status'] = None

    avg_show_rating = user_show_relation.objects.filter(show=show)
    average = 0
    counter = 0
    for status in avg_show_rating:
        counter = counter + 1
        average = average + status.rating
        average = average/counter

    context_dict['avg_show_rating'] = avg_show_rating
    context_dict['average'] = average


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

@login_required
def series_follow(request, tv_show_slug):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')
    try:
        show = tv_show.objects.get(show_slug=tv_show_slug)
        show_exists = True
        context_dict['show'] = show
    except:
        show_exists = False
        context_dict['show'] = None

    if show_exists:
        if userprofile.watchlist.filter(show_slug=tv_show_slug).exists():
            userprofile.watchlist.remove(show)
            added = False
            if user_show_relation.objects.filter(user=userprofile, show=show).exists():
                user_show_relation.get(user=userprofile, show=show).delete()
                deleted = True
            ep_rels = user_episode_relation.objects.filter(user=userprofile, show=show)
            if ep_rels.exists():
                for each in ep_rels:
                    each.delete()
        else:
            userprofile.watchlist.add(show)
            added = True

            episodes_from_show = episode.objects.filter(show_id=show)
            if episodes_from_show.exists():
                for each_episode in episodes_from_show:
                    rel = user_episode_relation()
                    rel.user = userprofile
                    rel.show = show
                    rel.episode = each_episode
                    rel.watched = False
                    rel.save()

    context_dict['added'] = added

    return render(request, 'tvtrail/series_follow.html', context_dict)

@login_required
def show_episode(request, tv_show_slug, season_param, episode_param):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

    try:
        show = tv_show.objects.get(show_slug=tv_show_slug)
        seasons = season.objects.get(show_name=show, season_num=season_param)
        episodes = episode.objects.filter(show_id=show, season_num=seasons)[int(episode_param)-1]
        context_dict['show'] = show
        context_dict['seasons'] = seasons
        context_dict['episodes'] = episodes
    except tv_show.DoesNotExist:
        context_dict['show'] = None
        context_dict['seasons'] = None
        context_dict['episodes'] = None

    try:
        episode_status = user_episode_relation.objects.get(user=userprofile, show=show, episode=episodes)
        context_dict['ep_status'] = episode_status
    except user_episode_relation.DoesNotExist:
        context_dict['ep_status'] = None

    avg_ep_rating = user_episode_relation.objects.filter(episode=episodes)
    average = 0
    counter = 0
    for rating in avg_ep_rating:
        counter = counter + 1
        average = average + rating.rating
        average = average/counter

    context_dict['avg_show_rating'] = avg_ep_rating
    context_dict['average'] = average

    return render(request, 'tvtrail/episode.html', context_dict)

def explore(request):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

    alphabet_list = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    context_dict['alphabet_list'] = alphabet_list

    return render(request, 'tvtrail/explore.html', context_dict)

def explore_alpha(request, alphabet):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

    alpha = alphabet
    context_dict['alphabet'] = alpha

    shows = tv_show.objects.order_by('show_name')
    filtered_shows = []
    for show in shows:
        if show.show_name[0] == alpha:
            filtered_shows.append(show)

    if len(filtered_shows) > 0:
        context_dict['sorted_shows'] = filtered_shows
    else:
        context_dict['sorted_shows'] = None
    #if len(filtered_shows) > 0:
    #    sorted_shows = sorted(filtered_shows)
    #    context_dict['sorted_shows'] = sorted_shows
    #else:
    #    context_dict['sorted_shows'] = None

    return render(request, 'tvtrail/explore_alpha.html', context_dict)

def genres(request):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

    genre_list = genre.objects.order_by('genre_name')

    if genre_list.exists():
        context_dict['genre_list'] = genre_list
    else:
        context_dict['genre_list'] = None

    return render(request, 'tvtrail/genres.html', context_dict)

def genre_shows(request, genre_param):
    context_dict = {}

    try:
        current_user = User.objects.get(username=request.user)
        context_dict['active_user'] = current_user
    except User.DoesNotExist:
        return redirect('index')
    try:
        userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
        context_dict['active_userprofile'] = userprofile
    except UserProfile.DoesNotExist:
        return redirect('index')

    try:
        current_genre = genre.objects.get(genre_name=genre_param)
        context_dict['genre'] = current_genre
    except genre.DoesNotExist:
        context_dict['genre'] = None

    if context_dict['genre'] != None:
        try:
            shows = tv_show.objects.filter(genres=current_genre).order_by('show_name')
            context_dict['shows'] = shows
        except tv_show.DoesNotExist:
            context_dict['shows'] = None
    else:
        context_dict['shows'] = None

    return render(request, 'tvtrail/genre_shows.html', context_dict)