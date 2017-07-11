from codeschool.api import router
from . import views

router.register('users', views.SentimentBoardViewSet)