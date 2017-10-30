from django.conf.urls import url
from django.conf.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset' , views.HelloViewSet, base_name = 'hello-viewset')
router.register('profile' , views.UserProfileViewSet)
router.register('login' , views.loginViewSet, base_name = 'login')
router.register('feed' , views.UserProfileFeedViewSet)
router.register('post' , views.UserPostViewSet)


urlpatterns = [
    url(r'^hello-view/' , views.HelloApiView.as_view()),
    url(r'', include(router.urls))
]
