from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('users', views.AppUserViewSet)
router.register('contents', views.ContentViewSet)
router.register('collections', views.CollectionViewSet)
router.register('history', views.HistoryViewSet, basename='history')
router.register('subscribers', views.SubscriberViewSet)
content_router = routers.NestedDefaultRouter(router, 'contents', lookup='content')
content_router.register('comments', views.CommentViewSet, basename='contents-comments')
content_router.register('likes', views.LikeViewSet, basename='contents-likes')
urlpatterns = router.urls + content_router.urls
