from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

# Create your models here.

class genre(models.Model):
    genre_id = models.IntegerField(default=1, unique=True, primary_key=True)
    genre_name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.genre_name

class tv_show(models.Model):
    show_id = models.IntegerField(default=None, primary_key=True, unique=True)
    show_name = models.CharField(max_length=512)
    year = models.IntegerField(default=2000)
    #avg_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    poster = models.ImageField(upload_to='series_posters', blank=True)
    genres = models.ManyToManyField(genre)
    synopsis = models.TextField(max_length=10000)
    show_slug = models.SlugField()
    followers = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.show_slug = slugify(self.show_name)
        super(tv_show, self).save(*args, **kwargs)

    def __str__(self):
        return self.show_name

    class Meta:
        verbose_name_plural = 'TV Shows'
        verbose_name = 'TV Show'

class season(models.Model):
    season_id = models.CharField(max_length=128, unique=True)
    show_name = models.ForeignKey(tv_show)
    season_num = models.IntegerField(default=1)

    def __str__(self):
        return str(self.season_num)

class episode(models.Model):
    episode_id = models.CharField(max_length=128, unique=True)
    show_id = models.ForeignKey(tv_show)
    season_num = models.ForeignKey(season)
    season_number = models.IntegerField(default=1)
    episode_title = models.CharField(max_length=256)
    episode_num = models.IntegerField(default=1)
    avg_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    runtime = models.IntegerField(default=20)
    airdate = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
    synopsis = models.TextField(max_length=10000)
    episode_slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.episode_slug = slugify(self.episode_title)
        super(episode, self).save(*args, **kwargs)

    def __str__(self):
        return self.episode_title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_pictures', blank=True)
    watchlist = models.ManyToManyField(tv_show, blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    

    def __str__(self):
        return self.user.username

class user_show_relation(models.Model):
    user = models.ForeignKey(UserProfile)
    show = models.ForeignKey(tv_show)
    rating = models.DecimalField(default=None, decimal_places=1, max_digits=2)

    def __str__(self):
        return str(self.rating)

class user_episode_relation(models.Model):
    user = models.ForeignKey(UserProfile)
    show = models.ForeignKey(tv_show)
    episode = models.ForeignKey(episode)
    #rating =  models.DecimalField(default=None, decimal_places=1, max_digits=2)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s %s' % (self.user, self.show, self.episode, self.watched)