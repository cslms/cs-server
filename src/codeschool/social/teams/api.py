from codeschool.api import router
from . import views

router.register('social/teams', views.TeamViewSet)
router.register('social/pairs', views.PairViewSet)
