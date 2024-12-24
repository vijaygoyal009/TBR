from rest_framework import serializers
from .models import Playground 
from auth_app.models import CustomUser , UserProfile

class PlaygroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playground
        fields = '__all__'




    


