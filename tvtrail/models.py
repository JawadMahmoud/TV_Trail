from django.db import models
from django.template.defaultfilters import slugify
import datetime

# Create your models here.

class tv_show(models.Model):
    show_id = models.CharField(primary_key=True, max_length=128, unique=True)
    show_name = models.CharField(max_length=512)
    year = models.IntegerField(default=2000)
    user_ratings = []
    avg_rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    poster = models.ImageField()
    genres = []
    synopsis = models.TextField(max_length=10000)
    show_slug = models.SlugField()

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
    epsiode_id = models.CharField(max_length=128, unique=True)
    show_id = models.ForeignKey(tv_show)
    season_num = models.ForeignKey(season)
    episode_title = models.CharField(max_length=256)
    episode_num = models.IntegerField(default=1)
    user_ratings = []
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

