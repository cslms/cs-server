import rules


@rules.predicate
def is_visitor(user, activity):
    """
    Users can view the activity if:

    * User is activity owner
    * Activity is visible
    """

    return activity.visible or activity.owner == user


@rules.predicate
def is_editor(user, activity):
    """
    The following users can edit an activity:

    * The superuser
    * The activity owner
    """
    return activity.owner == user


@rules.predicate
def is_inspector(user, activity):
    """
    The following users can inspect the content of an activity including
    student submissions and statistics:

    * The superuser
    * The activity owner
    """
    return is_editor(user, activity) or False

rules.add_perm('activities.edit_activity', is_editor)
rules.add_perm('activities.inspect_activity', is_inspector)
rules.add_perm('activities.view_submission', is_inspector)
rules.add_perm('activities.view_submission_stats', is_inspector)
