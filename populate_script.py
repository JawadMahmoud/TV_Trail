import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                    'tv_trail_project.settings')

import django
django.setup()
from tvtrail.models import tv_show, season, episode

def populate():

    