from codeschool.api import router
from . import views

router.register('organizations', views.OrganizationViewSet)
router.register('disciplines', views.DisciplinesViewSet)
