from codeschool.api import router
from . import views

router.register('programming-languages', views.ProgrammingLanguageViewSet)
router.register('file-format', views.FileFormatViewSet)
