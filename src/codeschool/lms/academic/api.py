from codeschool.api import router
from . import views

router.register('faculties', views.FacultyViewSet)
router.register('courses', views.CourseViewSet)
router.register('disciplines', views.DisciplinesViewSet)
