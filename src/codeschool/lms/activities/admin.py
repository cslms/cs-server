from django.contrib import admin
from codeschool.lms.activities.models import Progress, Submission, Feedback


admin.site.register(Progress)
admin.site.register(Submission)
admin.site.register(Feedback)
