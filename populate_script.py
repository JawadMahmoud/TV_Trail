import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'tv_trail_project.settings')

import django
django.setup()
from tvtrail.models import tv_show, season, episode, genre
from datetime import datetime
import tmdbsimple as tmdb
tmdb.API_KEY = 'ecffefd97cb0d5b7fe8ce74e5439ff1f'




def populate():


    a = 1
    while a<7:
            try: 
                show = tmdb.TV(a)
                response = show.info()
                tv_show_name = response['name']
                tv_show_id = response['id']
                tv_show_synopsis = response['overview']
                tv_show_poster = response['poster_path']
                tv_show_avg_rating = response['vote_average']
                tv_show_date = response['first_air_date']
                #print(tv_show_year)
                strip_date = datetime.strptime(tv_show_date, '%Y-%m-%d')
                strip_year = strip_date.year
                tv_show_year = int(strip_year)
                finallist = []
                genrelist = response['genres']
                for each in genrelist:
                    finallist.append(each['name'])
                    tv_show_genre = finallist
                add_show(tv_show_name, tv_show_id, tv_show_synopsis, tv_show_poster, tv_show_avg_rating, tv_show_year, tv_show_genre)
                a = a+1
            except: a = a+1
    a = 1
    b = 1
    while a<7:
        
            try:
                show = tmdb.TV(a)
                show_response = show.info()
                season = tmdb.TV_Seasons(a, b)
                response = season.info()
                tv_season_id = response['id']
                tv_season_number = response['season_number']
                tv_show_id = show_response['id']
                add_season(tv_show_id, tv_season_id, tv_season_number)
                b = b+1
            except:
                a = a+1
                b = 1
    a=1
    b=1
    c=1
    check = 1
    while a<7:
    
        try:
            show = tmdb.TV(a)
            show_response = show.info()
            season = tmdb.TV_Seasons(a, b)
            season_response = season.info()
            tv_season_id = season_response['id']
            episode = tmdb.TV_Episodes(a, b, c)
            response = episode.info()
            tv_episode_id = response['id']
            tv_episode_number = response['episode_number']
            tv_show_id = show_response['id']
            tv_episode_airdate = response['air_date']
            tv_episode_synopsis = response['overview']
            tv_episode_name = response['name']
            tv_episode_avg_rating = response['vote_average']
            tv_season_num = response['season_number']
            add_episode(tv_season_id, tv_show_id, tv_episode_id, tv_season_num, tv_episode_name, tv_episode_number, tv_episode_avg_rating, tv_episode_airdate, tv_episode_synopsis)
            c = c+1
            check = 1
        except:
            b = b + 1
            c = 1
            if check == 0:
                a = a + 1
                b = 1
            else: check = 0
def add_show(title, ID, Synopsis, Poster, Avg_rating, Year, Genres):
    s = tv_show.objects.get_or_create(show_name = title,)[0]
    s.show_id = ID
    s.synopsis = Synopsis
    s.poster = Poster
    s.avg_rating = Avg_rating
    s.year = Year
    for eachGenre in Genres:
        g = genre.objects.get_or_create(genre_name = eachGenre)[0]
        s.genres.add(g)

    print(s.show_name)
    s.save()
    return s
def add_season(title, ID, Number):
    s = tv_show.objects.get_or_create(show_id = title,)[0]
    S = season(show_name = s, season_id = ID, season_num = Number)
    print(S.show_name)
    S.save()
    return S
def add_episode(seasonID, showID, epID, sNum, epTitle, epNum, avgRate, Airdate, Synopsis):
    s = tv_show.objects.get_or_create(show_id = showID,)[0]
    a = season.objects.get_or_create(season_id = seasonID,)[0]
    S = episode(season_num = a, show_id = s, episode_id = epID, season_number = sNum, episode_title = epTitle, episode_num = epNum, avg_rating = avgRate, airdate = Airdate, synopsis = Synopsis)
    print(S.show_id)
    S.save()
    return S


# Start execution here!
if __name__ == '__main__':
    print("Starting tvtrail population script...")
    populate()
