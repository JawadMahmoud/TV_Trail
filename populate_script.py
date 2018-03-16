import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'tv_trail_project.settings')

import django
django.setup()
from tvtrail.models import tv_show, season, episode
from tmdbv3api import TMDb, TV
tmdb = TMDb()
tmdb.api_key = 'ecffefd97cb0d5b7fe8ce74e5439ff1f'


def populate():
    

    a = 1
    tv = TV()
    while a<1000000:
        m = tv.details(a)
        tv_show = tv.search(m.name)
        for result in tv_show:
            tv_show_name = result.name
            tv_show_id = result.id
            tv_show_synopsis = result.overview
            tv_show_poster = result.poster_path
            tv_show_avg_rating = result.vote_average
            
        add_show(tv_show_name, tv_show_id, tv_show_synopsis, tv_show_poster, tv_show_avg_rating)
        a = a+1
def add_show(title, ID, Synopsis, Poster, Avg_rating):
    s = tv_show.objects.get_or_create(show_name = title,)[0]
#    s = tv_show.objects.get_or_create(show_id = ID)
#    s = tv_show.objects.get_or_create()[0]
#    s = tv_show.objects.get_or_create(poster = Poster)[0]
 #   s = tv_show.objects.get_or_create(avg_rating = Avg_rating)[0]
    s.show_id = ID
    s.synopsis = Synopsis
    s.poster = Poster
    s.avg_rating = Avg_rating

    print(s.show_name)
    s.save()
    return s

# Start execution here!
if __name__ == '__main__':
    print("Starting tvtrail population script...")
    populate()
