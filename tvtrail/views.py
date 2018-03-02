from django.shortcuts import render
from django.http import HttpResponse
from tvtrail.models import tv_show, season, episode


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