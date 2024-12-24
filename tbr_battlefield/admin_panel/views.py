from django.shortcuts import render
from rest_framework import viewsets
from admin_panel.serializers import PlaygroundSerializer
from admin_panel.models import Playground
from auth_app.permissions import IsAdminUser
from auth_app.models import CustomUser , UserProfile , CoachProfile

class PlaygroundViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing, editing, and deleting Playground instances.
    """
    permission_classes = [IsAdminUser]
    queryset = Playground.objects.all()  # Fetch all Playground objects
    serializer_class = PlaygroundSerializer



