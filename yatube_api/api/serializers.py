from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', )
        model = User


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    comments = CommentSerializer(
        many=True,
        required=False
    )

    class Meta:
        model = Post
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        follower = self.context['request'].user
        following = data['following']

        if Follow.objects.filter(user=follower, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на данного автора'
            )

        if follower == following:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя'
            )

        return data

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow
