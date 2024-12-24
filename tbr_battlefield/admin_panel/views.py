from django.shortcuts import render
from rest_framework import viewsets
from admin_panel.serializers import PlaygroundSerializer , AdminUserSerializer , AdminCoachSerializer
from admin_panel.models import Playground
from auth_app.permissions import IsAdminUser
from auth_app.models import CustomUser


class PlaygroundViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = Playground.objects.all()  # Fetch all Playground objects
    serializer_class = PlaygroundSerializer




class AdminUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.filter(role='user')  # Only users
    serializer_class = AdminUserSerializer




class AdminCoachViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = CustomUser.objects.filter(role='coach')  # Only coaches
    serializer_class = AdminCoachSerializer



