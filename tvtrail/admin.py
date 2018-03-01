from django.contrib import admin
from tvtrail.models import tv_show, season, episode

# Register your models here.

class tv_showAdmin(admin.ModelAdmin):
    prepopulated_fields = {'show_slug':('show_name',)}

class episodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'episode_slug':('episode_title',)}

admin.site.register(tv_show, tv_showAdmin)
admin.site.register(season)
admin.site.register(episode, episodeAdmin)