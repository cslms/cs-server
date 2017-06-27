from codeschool.api import router
from . import views

router.register('config-options', views.ConfigOptionKeyValuePairViewSet)
router.register('server-data', views.DataEntryKeyValuePairViewSet)
