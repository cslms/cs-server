from codeschool.components.navbar import navbar


def activity_list_navbar(page, user):
    return navbar(admin=True, admin_perms='activities.edit_activity',
                  user=user, page=page)


def activity_section_navbar(page, user):
    return navbar(admin=True, admin_perms='activities.edit_activity',
                  user=user, page=page)
