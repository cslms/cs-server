from codeschool.api import router
from . import views

router.register('programming-languages', views.ProgrammingLanguageViewSet)
router.register('file-format', views.FileFormatViewSet)
router.register('config-options', views.ConfigOptionKeyValuePairViewSet)
router.register('server-data', views.DataEntryKeyValuePairViewSet)
