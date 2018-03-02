from django.contrib import admin
from tvtrail.models import tv_show, season, episode, genre, UserProfile
from tvtrail.models import user_show_relation, user_episode_relation

# Register your models here.

class tv_showAdmin(admin.ModelAdmin):
    prepopulated_fields = {'show_slug':('show_name',)}

class episodeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'episode_slug':('episode_title',)}

admin.site.register(tv_show, tv_showAdmin)
admin.site.register(season)
admin.site.register(episode, episodeAdmin)
admin.site.register(genre)
admin.site.register(UserProfile)
admin.site.register(user_show_relation)
admin.site.register(user_episode_relation)