from codeschool.api import router
from . import views


router.register('points', views.ScoreViewSet)
router.register('points/given', views.GivenPointsViewSet)