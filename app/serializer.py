from rest_framework import serializers
from .models import AppUser, Collection, Comment, Content, Subscriber, History, LikeItem


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'birth_date', 'phone_number', 'MEMBERSHIP_STATUS', 'user_id', 'subscribers_count']

    subscribers_count = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'user_id', 'content_id']

    content_id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        return Comment.objects.create(content_id=self.context['content_id'], user_id=self.context['user_id'],
                                      **validated_data)


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id', 'file', 'title', 'description', 'upload_date', 'collection', 'views_count', 'likes_count']

    views_count = serializers.IntegerField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    def create(self, validated_data):
        return Content.objects.create(app_user_id=self.context['user_id'], **validated_data)


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'app_user_id', 'user_id']

    user_id = serializers.IntegerField(read_only=True)
    app_user_id = serializers.IntegerField()

    def validate(self, attrs):
        if AppUser.objects.filter(user_id=self.context['user_id']).count() > 0:
            return serializers.ValidationError('first complete your user profile')
        return attrs

    def create(self, validated_data):
        return Subscriber.objects.create(user_id=self.context['user_id'], **validated_data)


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['id', 'content']

    content = ContentSerializer()


class LikeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeItem
        fields = ['id', 'user_id', 'content_id']
    user_id = serializers.IntegerField(read_only=True)
    content_id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        if LikeItem.objects.filter(user_id=self.context['user_id'], content_id=self.context['content_id']).exists():
            raise serializers.ValidationError('You have already Like this content')

        return LikeItem.objects.create(user_id=self.context['user_id'], content_id=self.context['content_id'])
