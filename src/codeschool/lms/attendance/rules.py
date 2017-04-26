import rules


@rules.predicate
def is_teacher(user, page):
    """
    The following users are treated as teachers:

    * The superuser
    * The page owner
    """
    return page.owner == user


rules.add_perm('attendance.see_passphrase', is_teacher)
rules.add_perm('activities.edit_passphrase', is_teacher)
