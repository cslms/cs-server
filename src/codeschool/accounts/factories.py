import datetime as dt
import random

import factory.django
from django.db import IntegrityError
from django.db.models import signals
from mommys_boy import DjangoMommyFactory, SubFactory, Faker

from codeschool.accounts import models
from codeschool.accounts.models import Profile
from codeschool.factories import fake

PROFILE_GENDER = {'male': Profile.GENDER_MALE, 'female': Profile.GENDER_FEMALE}


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


def make_user(username, email, password, update=False, commit=True, **kwargs):
    """
    Creates a user and sets its password.

    Non-user fields are passed to user profile.

    If update=True, update existing models instead of raising an error.

    If commit=False, do not save data to database uses only instance.
    """

    user_fields = {field.name for field in models.User._meta.fields}
    user_kwargs = {k: v for k, v in kwargs.items() if k in user_fields}
    profile_kwargs = {k: v for k, v in kwargs.items() if k not in user_fields}

    # Create user
    user = models.User(username=username, email=email, **user_kwargs)
    user.set_password(password)
    if commit:
        try:
            user.save()
        except IntegrityError:
            if not update:
                raise
            old = models.User.objects.get(username=username)
            user.id = old.id
            user.save()

    # Normalize arguments
    if 'gender' in profile_kwargs:
        value = profile_kwargs['gender']
        profile_kwargs['gender'] = PROFILE_GENDER.get(value, value)

    # Create profile
    profile = Profile(user=user, **profile_kwargs)
    try:
        profile.id = Profile.objects.get(user=user).id
    except Profile.DoesNotExist:
        pass
    if commit:
        profile.save()

    return user


def make_yoda_teacher():
    curr_date = dt.datetime.now().date()
    return make_user(
        update=True,
        is_teacher=True,
        username='yoda',
        first_name='Yoda',
        last_name='Master',
        password='thereisnotry',
        email='master.yoda@dagobah.com',
        gender='male',
        date_of_birth=curr_date - dt.timedelta(days=int(900 * 365.25))
    )


def make_girafales_teacher():
    return make_user(
        update=True,
        is_teacher=True,
        username='girafales123',
        first_name='Inocêncio',
        last_name='Girafales',
        password='florinda',
        email='girafales@chaves.com.mx',
        gender='male',
        about_me='A message to Dona Florinda, my love: I love you!',
        date_of_birth=birthday(45),
    )


def make_helena_teacher():
    return make_user(
        update=True,
        is_teacher=True,
        username='helena',
        first_name='Helena',
        last_name='Jacinta',
        password='carrosel',
        email='prof.helena@carrosel.mx',
        gender='female',
        date_of_birth=birthday(35),
    )


def make_miyagi_teacher():
    return make_user(
        update=True,
        is_teacher=True,
        username='prof.miyagi',
        first_name='Keisuke',
        last_name='Miyagi',
        password='karatekid',
        email='miyagi@karatekid.com',
        gender='male',
        date_of_birth=birthday(60),
    )


def make_joe_user():
    return make_user(
        update=True,
        username='joe',
        first_name='Joe',
        last_name='Smith',
        password='joe',
        email='joe@hotmail.com',
        gender='male',
        date_of_birth=birthday(),
    )


def make_random_student():
    gender = random.choice(['male', 'female'])
    if gender == 'male':
        name = fake.first_name_male()
    else:
        name = fake.first_name_female()
    try:
        return make_user(
            username=fake.user_name(),
            first_name=name,
            last_name=fake.last_name(),
            password=fake.password(),
            email=fake.email(),
            gender=gender,
            date_of_birth=birthday(),
        )
    except IntegrityError:
        pass


def make_maurice_moss():
    return make_user(
        update=True,
        username='admin',
        first_name='Maurice',
        last_name='Moss',
        password='admin',
        nickname='moss',
        phone='555-123-456',
        website='http://www.channel4.com/programmes/the-it-crowd',
        about_me='Knows everything about "The Internet".',
        email='moss@reynholm.co.uk',
        gender='male',
        date_of_birth=birthday(28),
    )


def make_mr_robot():
    return make_user(
        update=True,
        username='mr_robot',
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


def make_teachers():
    teachers = [
        make_yoda_teacher(),
        make_helena_teacher(),
        make_girafales_teacher(),
        make_miyagi_teacher()
    ]
    ids = [x.id for x in teachers]
    return models.User.objects.filter(id__in=ids)


def make_students(size=5):
    students = [make_random_student() for _ in range(size)]
    ids = [x.id for x in students]
    return models.User.objects.filter(id__in=ids)
