from lazyutils import delegate_to


class FromProgressAttributesMixin:
    """
    Mixin class for submissions and feedback.

    Imports attributes from obj.progress
    """

    activity = delegate_to('progress', readonly=True)
    activity_id = delegate_to('progress', readonly=True)
    activity_title = property(lambda x: x.progress.activity_page.title)
    user = delegate_to('progress', readonly=True)
