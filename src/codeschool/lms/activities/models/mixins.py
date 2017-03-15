class HasProgressMixin:
    activity = property(lambda x: x.progress.activity)
    activity_id = property(lambda x: x.progress.activity_id)
    activity_title = property(lambda x: x.progress.activity_page.title)
    user = property(lambda x: x.progress.user)
    sender_username = property(lambda x: x.progress.user.username)