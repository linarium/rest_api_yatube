from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Group, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    post = SlugRelatedField(
        read_only=True,
        slug_field='pk',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Follow.objects.filter(
            user=self.context['request'].user, following=value
        ).exists():
            raise serializers.ValidationError(
                'Нельзя подписаться на пользователя дважды'
            )
        return value

    class Meta:
        model = Follow
        fields = ('user', 'following')
