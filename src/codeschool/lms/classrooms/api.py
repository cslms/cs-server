from codeschool.api import router
from . import views

router.register('classrooms', views.ClassroomViewSet)
