from sulfur import urlchecker


def test_basic_routes(user, request_with_user):
    context = {'username': user.username}
    urls = [
        '/auth/{username}',
        '/auth/{username}/edit',
        '/auth/{username}/password',
    ]
    urlchecker.check_url(urls, context, html5=True)