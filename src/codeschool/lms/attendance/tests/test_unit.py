import time

import mock
import model_mommy.mommy
import mommys_boy
import pytest
from django.contrib.auth.models import User

from codeschool.lms.attendance import models


@pytest.fixture
def sheet():
    return mommys_boy.mommy.prepare(models.AttendanceSheet, id=1)


@pytest.fixture
def event(sheet):
    return sheet.new_event(commit=False)


@pytest.fixture
@mock.patch('codeschool.lms.attendance.models.AttendancePage.owner', 'user')
def page(sheet):
    page = models.AttendancePage(id=1)
    page._attendance_sheet = sheet
    return page


def test_create_new_event(sheet):
    event = sheet.new_event(commit=False)
    assert event.passphrase
    assert event.expires > event.created
    assert event.passphrase == sheet.current_passphrase()
    assert event is sheet.current_event()


def test_update_passphrase(event):
    passphrase = event.passphrase
    expires = event.expires
    time.sleep(2e-6)
    event.update(commit=False)
    assert event.passphrase != passphrase
    assert event.expires > expires


def test_new_event_is_never_expired(sheet, event):
    assert abs(sheet.minutes_left() - sheet.expiration_minutes) < 1e-3
    assert sheet.is_expired() is False


def test_expired_event(sheet, event):
    event.expires = event.created
    assert sheet.is_expired() is True


def test_passphrase_validator(sheet, event):
    assert sheet.is_valid(event.passphrase) is True
    assert sheet.is_valid(event.passphrase + 'error') is False


def test_page_clean(page):
    page.clean()
    assert page.title
    assert page.attendance_sheet


def test_page_generate_context(page, event):
    path = 'codeschool.lms.attendance.models.AttendanceSheet.current_event'
    with mock.patch(path, lambda s: event):
        ctx = page.get_context(mock.Mock())
    assert ctx['is_expired'] is False
    assert ({'page', 'form', 'is_teacher'}).issubset(ctx.keys())
