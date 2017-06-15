from codeschool.api import router

from . import views

router.register('friendship-requests', views.FriendshipRequestViewSet)
router.register('friends', views.FriendViewSet)
router.register('followers', views.FollowerViewSet)
router.register('followees', views.FolloweeViewSet)
