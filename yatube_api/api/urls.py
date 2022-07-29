from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router_v1 = DefaultRouter()
router_v1.register(r'users', views.UserViewSet)
router_v1.register(r'posts', views.PostViewSet)
router_v1.register(r'groups', views.GroupViewSet)
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)
router_v1.register(r'follow', views.FollowViewSet, basename='follow')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
