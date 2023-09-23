from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

PKEY = "ctam2023"

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name',)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'groups', 'is_staff',)

class UpdateUserSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    user_id = serializers.IntegerField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Identifiants incorrects")


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_staff')
        # add other fields
        extra_kwargs = {'password': {'write_only': True}, 'mission': {'write_only': True}}


    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], username=validated_data['email'], password=PKEY,
                                        first_name=validated_data['first_name'], last_name=validated_data['last_name'], is_staff=validated_data['is_staff'])
        return user


class UserMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
