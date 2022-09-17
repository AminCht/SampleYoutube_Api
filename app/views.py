from django.db.models import Count, F, Func, Value
from django.shortcuts import render
from django.http import HttpResponse
from .permissions import HistoryPermission
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import AppUser, Content, Comment, Collection, Subscriber, History, LikeItem
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .pagination import DefaultPagination
from .serializer import AppUserSerializer, CollectionSerializer, CommentSerializer, ContentSerializer, \
    SubscriberSerializer, HistorySerializer, LikeItemSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.


class AppUserViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    queryset = AppUser.objects.annotate(subscribers_count=Count('subscribers')).all()
    serializer_class = AppUserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user__first_name', 'user_id']
    ordering_fields = ['subscribers_count']
    pagination_class = DefaultPagination

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = AppUser.objects.get_or_create(user_id=self.request.user.id)
        if request.method == 'GET':
            serializer = AppUserSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AppUserSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    pagination_class = DefaultPagination

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE', 'PUT']:
            return [IsAdminUser()]
        return [AllowAny()]

    def destroy(self, request, *args, **kwargs):
        if Content.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'collection can not be deleted because it has some contents'})
        return super().destroy(request, *args, **kwargs)


class ContentViewSet(ModelViewSet):
    queryset = Content.objects.annotate(views_count=Count('history'), likes_count=Count('likeitem')).all()
    serializer_class = ContentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if History.objects.filter(content=instance, user_id=self.request.user.id).count() == 0:
            History.objects.create(content=instance, user_id=self.request.user.id)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    pagination_class = DefaultPagination

    def get_serializer_context(self):
        return {'content_id': self.kwargs['content_pk'], 'user_id': self.request.user.id}


class SubscriberViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class HistoryViewSet(ListModelMixin, DestroyModelMixin, GenericViewSet):
    def get_queryset(self):
        return History.objects.filter(user_id=self.request.user.id)
    serializer_class = HistorySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated, HistoryPermission]


class LikeViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    def get_queryset(self):
        return AppUser.objects.filter(user__likeitem__content_id=self.kwargs['content_pk'])
    serializer_class = LikeItemSerializer
    permission_classes = [IsAuthenticated]


    def get_serializer_context(self):
        return {'user_id': self.request.user.id, 'content_id': self.kwargs['content_pk']}


