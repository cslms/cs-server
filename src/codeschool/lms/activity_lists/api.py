from codeschool.api import router
from . import views

router.register('activity-lists', views.ActivityListViewSet)
router.register('activity-sections', views.ActivitySectionViewSet)