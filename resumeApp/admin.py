from django.contrib import admin
from .models import *

admin.site.site_header = admin.site.site_title = "Resume App Admin"

# admin.site.register(Master)
# admin.site.register(UserProfile)
# admin.site.register(Education)
# admin.site.register(Experience)
# admin.site.register(Reference)
# admin.site.register(Skill)
# admin.site.register(Project)

import resumeApp.models as models

for m in models.__dict__.values():
    if 'is_model' in dir(m):
        admin.site.register(m)