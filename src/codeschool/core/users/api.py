from codeschool.api import router
from . import viewsets

router.register('users', viewsets.UserViewSet)