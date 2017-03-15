from django.contrib import admin
from codeschool.lms.activities.models import *


admin.site.register(ActivityList)
admin.site.register(ActivitySection)
admin.site.register(Progress)
admin.site.register(Submission)
admin.site.register(Feedback)
