from rest_framework import serializers
from .models import CustomUser, AdminProfile, CoachProfile, UserProfile


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Explicitly setting the role to 'user'
        validated_data['role'] = 'user'
        user = CustomUser.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user





class CoachSignupSerializer(serializers.ModelSerializer):
    experience = serializers.IntegerField()
    bio = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'mobile', 'password', 'experience', 'bio']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        experience = validated_data.pop('experience')
        bio = validated_data.pop('bio')
        user = CustomUser.objects.create_user(**validated_data, role='coach')
        validated_data['role'] = 'coach'

        CoachProfile.objects.create(user=user, experience=experience, bio=bio)
        return user






class AdminSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'mobile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Explicitly setting the role to 'admin'
        user = CustomUser.objects.create_superuser(**validated_data)
        AdminProfile.objects.create(user=user)  # Create AdminProfile entry
        return user
