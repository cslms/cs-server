import datetime as dt
import string

import factory.django
import random
from django.db import IntegrityError
from django.db.models import signals
from mommys_boy import DjangoMommyFactory, SubFactory, Faker

from codeschool.factories import fake
from . import models

PROFILE_GENDER = {
    'male': models.Profile.GENDER_MALE,
    'female': models.Profile.GENDER_FEMALE,
}


@factory.django.mute_signals(signals.pre_save, signals.post_save)
class UserFactory(DjangoMommyFactory):
    class Meta:
        model = models.User
        recipe = 'global'


class FullUserFactory(DjangoMommyFactory):
    class Meta:
        model = models.User
        recipe = 'global'


class ProfileFactory(DjangoMommyFactory):
    class Meta:
        model = models.Profile

    user = SubFactory(UserFactory)
    phone = Faker('phone_number')


def birthday(age=None):
    """
    A plausible random birth date for someone in the 15 to 60 years age range.
    """

    if age is None:
        age = random.randint(0, 60)
    day = random.randint(0, 365)
    year = dt.datetime.now().year - age
    return dt.date(year, 1, 1) + dt.timedelta(days=day)


def make_user(alias, email, password, update=False, commit=True,
              school_id=None, is_teacher=False, **kwargs):
    """
    Creates a user and sets its password.

    Non-user fields are passed to user profile.

    If update=True, update existing models instead of raising an error.

    If commit=False, do not save data to database uses only instance.
    """

    user_fields = {field.name for field in models.User._meta.fields}
    user_fields.update(['first_name', 'last_name'])
    user_kwargs = {k: v for k, v in kwargs.items() if k in user_fields}
    profile_kwargs = {k: v for k, v in kwargs.items() if k not in user_fields}

    # Sets school id
    if school_id is None:
        school_id = random_school_id()
    user_kwargs.update(alias=alias, email=email, school_id=school_id)

    # Set role
    if is_teacher:
        user_kwargs.update(role=models.User.ROLE_TEACHER)

    # Fix name = first_name + last_name
    if 'first_name' in user_kwargs:
        user_kwargs['name'] = user_kwargs.pop('first_name')
        if 'last_name' in user_kwargs:
            user_kwargs['name'] += ' ' + user_kwargs.pop('last_name')

    # Create user
    user = models.User(**user_kwargs)
    user.set_password(password)
    if commit:
        try:
            user.save()
        except IntegrityError:
            if not update:
                raise
            old = models.User.objects.get(alias=alias)
            user.id = old.id
            user.save()

    # Normalize arguments
    if 'gender' in profile_kwargs:
        value = profile_kwargs['gender']
        profile_kwargs['gender'] = PROFILE_GENDER.get(value, value)

    # Create profile
    profile = models.Profile(user=user, **profile_kwargs)
    if commit:
        try:
            profile.id = models.Profile.objects.get(user=user).id
        except models.Profile.DoesNotExist:
            pass
        else:
            profile.save()
    else:
        user.profile = profile
    return user


def random_school_id():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(10))


def make_yoda_teacher(commit=True):
    curr_date = dt.datetime.now().date()
    return make_user(
        update=True,
        commit=commit,
        is_teacher=True,
        alias='yoda',
        name='Yoda',
        password='thereisnotry',
        email='master.yoda@dagobah.com',
        gender='male',
        date_of_birth=curr_date - dt.timedelta(days=int(900 * 365.25))
    )


def make_girafales_teacher(commit=True):
    return make_user(
        update=True,
        is_teacher=True,
        commit=commit,
        alias='girafales123',
        first_name='Inocêncio',
        last_name='Girafales',
        password='florinda',
        email='girafales@chaves.com.mx',
        gender='male',
        about_me='A message to Dona Florinda, my love: I love you!',
        date_of_birth=birthday(45),
    )


def make_helena_teacher(commit=True):
    return make_user(
        update=True,
        is_teacher=True,
        commit=commit,
        alias='helena',
        first_name='Helena',
        last_name='Jacinta',
        password='carrosel',
        email='prof.helena@carrosel.mx',
        gender='female',
        date_of_birth=birthday(35),
    )


def make_miyagi_teacher(commit=True):
    return make_user(
        update=True,
        is_teacher=True,
        commit=commit,
        alias='prof.miyagi',
        first_name='Keisuke',
        last_name='Miyagi',
        password='karatekid',
        email='miyagi@karatekid.com',
        gender='male',
        date_of_birth=birthday(60),
    )


def make_joe_user(commit=True):
    return make_user(
        update=True,
        alias='joe',
        first_name='Joe',
        last_name='Smith',
        commit=commit,
        password='joe',
        email='joe@hotmail.com',
        gender='male',
        date_of_birth=birthday(),
    )


def make_random_student(commit=True):
    gender = random.choice(['male', 'female'])
    if gender == 'male':
        name = fake.first_name_male()
    else:
        name = fake.first_name_female()
    try:
        return make_user(
            alias=fake.user_name(),
            first_name=name,
            last_name=fake.last_name(),
            commit=commit,
            password=fake.password(),
            email=fake.email(),
            gender=gender,
            date_of_birth=birthday(),
        )
    except IntegrityError:
        pass


def make_maurice_moss(commit=True):
    return make_user(
        update=True,
        alias='admin',
        first_name='Maurice',
        last_name='Moss',
        commit=commit,
        password='admin',
        nickname='moss',
        phone='555-123-456',
        website='http://www.channel4.com/programmes/the-it-crowd',
        about_me='Knows everything about "The Internet".',
        email='moss@reynholm.co.uk',
        gender='male',
        date_of_birth=birthday(28),
    )


def make_mr_robot(commit=True):
    return make_user(
        update=True,
        alias='mr_robot',
        commit=commit,
        first_name='<script>alert("you\'ve been pwnd!")</script>',
        last_name='<script>alert("you\'ve been pwnd!")</script>',
        password='robot',
        nickname='<script>alert("you\'ve been pwnd!")</script>',
        phone='555-123-456',
        website='http://www.channel4.com/programmes/the-it-crowd',
        about_me='<script>alert("you\'ve been pwnd!")</script>',
        email='robot@mr.robot.com',
        gender='male',
        date_of_birth=birthday(28),
    )


def make_teachers(commit=True):
    return [
        make_yoda_teacher(commit=commit),
        make_helena_teacher(commit=commit),
        make_girafales_teacher(commit=commit),
        make_miyagi_teacher(commit=commit)
    ]


def make_students(size=5, commit=True):
    return [make_random_student(commit=commit) for _ in range(size)]
