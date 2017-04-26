def test_basic_urls(user, client):
    context = {'username': user.username}
    urls = [
        '/auth/{username}',
        '/auth/{username}/edit',
        '/auth/{username}/password',
    ]
    client.check_url(urls, context, html5=True)


def _test_login_with_valid_user(driver, user_with_password, password):
    user = user_with_password
    driver.open('/')
