from rest_framework import serializers
from .models import User, Music, Movie


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializes registration requests and creates a new user."""
    password = serializers.CharField(write_only=True, required=False, )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User.objects.create(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MusicSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Music
        fields = ('id', 'category', 'title')


class MovieSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.title', read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'category', 'title')
