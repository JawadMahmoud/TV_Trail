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
from django.template.defaulttags import register
import datetime
from django.db.models import F


# Create your views here.
@login_required
def index(request):
    context_dict = {}

    current_user = User.objects.get(username=request.user)
    context_dict['active_user'] = current_user

    userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
    context_dict['active_userprofile'] = userprofile

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)
    
    followed_shows = userprofile.watchlist.all()
    upcoming_episodes = []
    ep_show_rel = {}
    #ep_season_rel = {}

    if followed_shows.exists():
        for show in followed_shows:
            try:
                latest_episode = episode.objects.filter(show_id=show, airdate__range=[datetime.datetime.now().date(), datetime.datetime.now().date() + datetime.timedelta(days=7)]).order_by('airdate')[0]
                #print(latest_episode)
                #ep_show_rel[latest_episode] = show.show_slug
                #ep_season_rel[latest_episode] = latest_episode.season_num
            except:
                latest_episode = None
            if latest_episode != None:
                ep_show_rel[latest_episode] = show.show_slug
                ep_status = user_episode_relation.objects.get(user=userprofile, episode=latest_episode, show=latest_episode.show_id)
                if ep_status.watched == False:
                    upcoming_episodes.append(latest_episode)
                #upcoming_episodes.append(latest_episode)
    
    if len(upcoming_episodes) > 0:
        context_dict['upcoming'] = upcoming_episodes
    else:
        context_dict['upcoming'] = None

    context_dict['ep_show'] = ep_show_rel
    #context_dict['ep_season'] = ep_season_rel

    popular_shows = tv_show.objects.filter(followers__gt=0).order_by('-followers')[:5]

    if popular_shows != None:
        context_dict['popular_five'] = popular_shows
    else:
        context_dict['popular_five'] = None

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

    episode_count = episode.objects.filter(show_id=show).count()

    context_dict['ep_count'] = episode_count
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
    context_dict = {}
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'picture': userprofile.picture, 'watchlist': userprofile.watchlist})

    current_user = User.objects.get(username=request.user)
    current_userprofile = UserProfile.objects.get_or_create(user=current_user)[0]


    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    followed_shows = userprofile.watchlist.all()
    #total_series_followed = current_userprofile.watchlist.all.count()


    total_ep_count = {}
    watched_ep_count = {}
    completion = {}

    all_ep_count = 0
    all_watch_count = 0
    all_completion = 0

    total_time_watched = 0
    total_time_left = 0

    for show in followed_shows:
        #print(show.show_name)
        watch_count = user_episode_relation.objects.filter(user=userprofile, show=show, watched=True).count()
        all_watch_count = all_watch_count + watch_count
        watched_ep_count[show.show_name] = watch_count

        ep_count = episode.objects.filter(show_id=show).count()
        all_ep_count = all_ep_count + ep_count
        total_ep_count[show.show_name] = ep_count
        #print(total_ep_count[show.show_name])

        if ep_count > 0:
            all_episodes = episode.objects.filter(show_id=show)
            for episode_in_show in all_episodes:
                episode_in_show_status = user_episode_relation.objects.get(user=current_userprofile, episode=episode_in_show)
                if episode_in_show_status.watched == True:
                    total_time_watched = total_time_watched + episode_in_show.runtime
                elif episode_in_show_status.watched == False:
                    total_time_left = total_time_left + episode_in_show.runtime
            completion[show.show_name] = (watch_count/ep_count)*100
        else:
            completion[show.show_name] = None

        if all_ep_count > 0:
            all_completion = round(((all_watch_count/all_ep_count)*100),1)
        else:
            all_completion = 0

    context_dict['total_episodes_list'] = total_ep_count
    context_dict['watch_episodes_list'] = watched_ep_count
    context_dict['completion_percentage'] = completion

    context_dict['total_completion_percentage'] = all_completion

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    context_dict['userprofile'] = userprofile
    context_dict['selected_user'] = user
    context_dict['current_user'] = current_user
    context_dict['current_userprofile'] = current_userprofile
    context_dict['form'] = form

    #print(total_ep_count)
    #print(userprofile.watchlist.all())

    ##### STATS
    context_dict['total_episodes_watched'] = all_watch_count
    context_dict['total_time_spent_watching'] = total_time_watched
    context_dict['total_time_for_completion'] = total_time_left
    #context_dict['total_series_followed'] = total_series_followed

    return render(request, 'tvtrail/profile.html', context_dict)

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
            
            tv_show.objects.filter(show_id=show.show_id).update(followers=F('followers') - 1)
            #show.update(followers=F('followers') - 1)
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
            
            tv_show.objects.filter(show_id=show.show_id).update(followers=F('followers') + 1)
            #show.update(followers=F('followers') + 1)

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
        print(episodes)
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

    #avg_ep_rating = user_episode_relation.objects.filter(episode=episodes)
    #average = 0
    #counter = 0
    #for rating in avg_ep_rating:
    #    counter = counter + 1
    #    average = average + rating.rating
    #    average = average/counter

    #context_dict['avg_show_rating'] = avg_ep_rating
    #context_dict['average'] = average

    return render(request, 'tvtrail/episode.html', context_dict)

@login_required
def episode_watch(request, tv_show_slug, season_param, episode_param):
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
        status_exists = True
        context_dict['ep_status'] = episode_status
    except user_episode_relation.DoesNotExist:
        status_exists = False
        context_dict['ep_status'] = None

    if status_exists:
        if episode_status.watched:
            set_watched = False
            episode_status.watched = False
            episode_status.save()

        elif not episode_status.watched:
            set_watched = True
            episode_status.watched = True
            episode_status.save()
    else:
        context_dict['set_watched'] = None

    context_dict['set_watched'] = set_watched

    return render(request, 'tvtrail/episode_watch.html', context_dict)

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

def search_form(request):
    return render(request, "tvtrail/search_form.html")

def search(request):
    context_dict = {}

    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        context_dict['query'] = q
        shows = tv_show.objects.filter(show_name__icontains=q)
        if shows.exists():
            context_dict['shows'] = shows
        else:
            context_dict['shows'] = None
        return render(request, 'tvtrail/search_results.html', context_dict)
    else:
        return HttpResponse('Please submit a search term.')

def upcoming(request):
    context_dict = {}

    current_user = User.objects.get(username=request.user)
    context_dict['active_user'] = current_user

    userprofile = UserProfile.objects.get_or_create(user=current_user)[0]
    context_dict['active_userprofile'] = userprofile

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)
    
    followed_shows = userprofile.watchlist.all()
    upcoming_episodes = []
    ep_show_rel = {}
    today = datetime.datetime.now().date()
    date_list = []
    days_index = 0
    while days_index < 7:
        date_list.append(today + datetime.timedelta(days=days_index))
        days_index = days_index + 1

    for each in date_list:
        print(each)

    #ep_season_rel = {}

    if followed_shows.exists():
        for show in followed_shows:
            try:
                #latest_episode = episode.objects.filter(show_id=show, airdate__range=[today, today + datetime.timedelta(days=7)]).order_by('airdate')[0]
                latest_episode = episode.objects.filter(show_id=show, airdate__gte=today).order_by('airdate')[0]
                #print(latest_episode)
                #ep_show_rel[latest_episode] = show.show_slug
                #ep_season_rel[latest_episode] = latest_episode.season_num
            except:
                latest_episode = None
            if latest_episode != None:
                ep_show_rel[latest_episode] = show.show_slug
                ep_status = user_episode_relation.objects.get(user=userprofile, episode=latest_episode, show=latest_episode.show_id)
                print(latest_episode.airdate)
                if ep_status.watched == False:
                    upcoming_episodes.append(latest_episode)
                #upcoming_episodes.append(latest_episode)
    
    if len(upcoming_episodes) > 0:
        context_dict['upcoming'] = upcoming_episodes
    else:
        context_dict['upcoming'] = None

    context_dict['ep_show'] = ep_show_rel
    context_dict['date_list'] = date_list

    return render(request, 'tvtrail/upcoming.html', context_dict)