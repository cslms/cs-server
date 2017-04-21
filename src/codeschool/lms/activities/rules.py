import rules


@rules.predicate
def is_activity_editor(user, activity):
    """
    The following users can edit an activity:

    * The superuser
    * The activity owner
    """
    return activity.owner == user


@rules.predicate
def is_activity_inspector(user, activity):
    """
    The following users can inspect the content of an activity including
    student submissions and statistics:

    * The superuser
    * The activity owner
    """
    return is_activity_editor(user, activity) or False


rules.add_perm('activities.edit_activity', is_activity_editor)
rules.add_perm('activities.inspect_activity', is_activity_inspector)
rules.add_perm('activities.view_submission_stats', is_activity_inspector)
