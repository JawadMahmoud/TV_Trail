from django.contrib import admin
from tvtrail.models import tv_show, season, episode

# Register your models here.

admin.site.register(tv_show)
admin.site.register(season)
admin.site.register(episode)