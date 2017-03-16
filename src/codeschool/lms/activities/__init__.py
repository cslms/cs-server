"""
====================
Activities Framework
====================

Codeschool defines abstract entities called activities that are the basis of
most interactions between students with the learning content. Activities can be
questions, homework, challenges or even very simple things such as a "download
activity" in which the student has to visit a page to download content.

Each activity has a definite URL handled by Wagtail and may be in several
places within the Wagtail URL hierarchical structure.

Interaction with activities
===========================

When a student opens an activity page, it automatically opens or creates a
Progress object that helps tracks students responses to the given activity.
In simple activities, the Session may last for a single request, but more
complex interactions spanning several requests are also possible.

Once the session finishes, it becomes marked for manual grading --if required--,
or it may compute the final grade for the student using data from all
intermediate response objects.
"""

default_app_config = 'codeschool.lms.activities.apps.ActivitiesConfig'
