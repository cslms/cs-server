import pytest


@pytest.mark.skip('wait for sulfur driver')
@pytest.mark.ui
class TestUI:
    def test_login_with_valid_user(self, driver, user_with_password, password):
        user = user_with_password
        driver.open('/')