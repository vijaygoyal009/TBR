from rest_framework import serializers
from .models import Playground 
from auth_app.models import CustomUser , UserProfile , CoachProfile

class PlaygroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playground
        fields = '__all__'



class AdminUserSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(required=False)  # Optional for updates

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'mobile', 'role', 'dob', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Optional for updates
        }

    def create(self, validated_data):
        dob = validated_data.pop('dob', None)
        user = CustomUser.objects.create_user(**validated_data, role='user')
        if dob:
            UserProfile.objects.create(user=user, dob=dob)  # `dob` ko UserProfile me save karo
        return user

    def update(self, instance, validated_data):
        dob = validated_data.pop('dob', None)
        for attr, value in validated_data.items():
            if attr == 'password' and value:
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        if dob:
            if hasattr(instance, 'user_profile'):
                instance.user_profile.dob = dob  # Agar UserProfile hai to dob update karo
                instance.user_profile.save()
            else:
                UserProfile.objects.create(user=instance, dob=dob)  # Agar UserProfile nahi hai to naya create karo
        return instance

    def to_representation(self, instance):
        # Yahan pe dob ko manual tarike se add kiya jaa raha hai response me
        representation = super().to_representation(instance)
        # Agar UserProfile me dob hai to wo include karo
        if hasattr(instance, 'user_profile') and instance.user_profile.dob:
            representation['dob'] = instance.user_profile.dob
        return representation





class AdminCoachSerializer(serializers.ModelSerializer):
    dob = serializers.DateField(required=False)  # Optional for updates
    experience = serializers.IntegerField(required=False)  # Optional for updates
    bio = serializers.CharField(required=False, allow_blank=True)  # Optional for updates

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'mobile', 'role', 'dob', 'experience', 'bio', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Optional for updates
        }

    def create(self, validated_data):
        dob = validated_data.pop('dob', None)
        experience = validated_data.pop('experience', None)
        bio = validated_data.pop('bio', None)

        # Create the user with role 'coach'
        user = CustomUser.objects.create_user(**validated_data, role='coach')

        # Create CoachProfile if necessary fields are provided
        if dob or experience or bio:
            CoachProfile.objects.create(user=user, dob=dob, experience=experience, bio=bio)

        return user

    def update(self, instance, validated_data):
        dob = validated_data.pop('dob', None)
        experience = validated_data.pop('experience', None)
        bio = validated_data.pop('bio', None)

        # Update the user fields (excluding password)
        for attr, value in validated_data.items():
            if attr == 'password' and value:
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        # Handle update for the CoachProfile model
        if hasattr(instance, 'coach_profile'):
            if dob:
                instance.coach_profile.dob = dob
            if experience is not None:
                instance.coach_profile.experience = experience
            if bio is not None:
                instance.coach_profile.bio = bio
            instance.coach_profile.save()
        else:
            # If no profile exists, create a new one
            CoachProfile.objects.create(user=instance, dob=dob, experience=experience, bio=bio)

        return instance

    def to_representation(self, instance):
        # Get the default representation first
        representation = super().to_representation(instance)

        # Include CoachProfile fields in the response
        if hasattr(instance, 'coach_profile'):
            representation['dob'] = instance.coach_profile.dob
            representation['experience'] = instance.coach_profile.experience
            representation['bio'] = instance.coach_profile.bio

        return representation
