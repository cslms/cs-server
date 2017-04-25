import rules


@rules.predicate
def is_registered(user, classroom):
    """
    Users that are considered to be registered in a classroom

    * The teacher.
    * All staff members.
    * All registered students.
    """
    return is_staff(user, classroom) or \
           classroom.students.filter(id=user.id).exists()


@rules.predicate
def is_staff(user, classroom):
    """
    Users with staff privileges.

    * The teacher.
    * Staff members.
    """
    return is_owner(user, classroom) or \
           classroom.staff.filter(id=user.id).exists()


@rules.predicate
def is_owner(user, classroom):
    """
    Users that own a classroom resource and can edit.

    * The teacher.
    """
    return classroom.owner == user or classroom.teacher == user


@rules.predicate
def is_colleague_of(user1, user2):
    """
    True if two users are colleagues (i.e., both are students in the same
    classroom).
    """
    return NotImplemented


@rules.predicate
def is_teacher_of(teacher, student):
    """
    True if first user is a teacher in a course in which the second user is a
    student.
    """
    return NotImplemented


@rules.predicate
def is_student_of(user1, user2):
    """
    True if first user is a student in a course in which the second user is a
    teacher.
    """
    return NotImplemented


rules.add_perm('classrooms.view_classroom', is_registered)
