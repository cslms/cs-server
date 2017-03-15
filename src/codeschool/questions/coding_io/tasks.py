from celery import shared_task


@shared_task
def test_task(*args, **kwargs):
    print('task called with %s args and %s kwargs' % (args, kwargs))
