from django.shortcuts import render
from rest_framework import viewsets
from admin_panel.serializers import PlaygroundSerializer , AdminUserSerializer , AdminCoachSerializer , TimeSlotSerializer
from admin_panel.models import Playground , TimeSlot
from auth_app.permissions import IsAdminUser
from auth_app.models import CustomUser
from rest_framework.response import Response
from datetime import timedelta, time
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status



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



class TimeSlotAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Get all time slots or a specific time slot by id
        """
        slot_id = kwargs.get('id', None)
        
        if slot_id:
            try:
                time_slot = TimeSlot.objects.get(id=slot_id)
            except TimeSlot.DoesNotExist:
                return Response({"error": "TimeSlot not found."}, status=status.HTTP_404_NOT_FOUND)
                
            return Response(TimeSlotSerializer(time_slot).data)

        time_slots = TimeSlot.objects.all()
        return Response(TimeSlotSerializer(time_slots, many=True).data)




    def post(self, request, *args, **kwargs):
        playground_id = request.data.get('playground_id')
        # List of age groups for which we need to create time slots
        age_groups = request.data.get('age_group', [])  # e.g., ["0-8", "9-10", "11-12", ...]
        time_slot_duration = request.data.get('time_slot_duration', 60)  # Default 60 minutes per slot
        
        try:
            playground = Playground.objects.get(id=playground_id)
        except Playground.DoesNotExist:
            return Response({"error": "Playground not found."}, status=404)

        # Time range for slots creation (4 PM to 9 PM)
        start_hour = 16  # 4 PM
        end_hour = 21  # 9 PM

        # Calculate the date range from registration start to end date
        current_date = playground.playground_registration_start_date
        end_date = playground.playground_registration_end_date  # Use correct end date

        created_slots = []
        
        # Loop through the entire date range
        while current_date <= end_date:
            # Loop over each age group
            for index, age_group in enumerate(age_groups):
                # Determine the time slot start and end time based on index
                start_time = time(start_hour + index, 0)  # Slot starts at 4 PM, 5 PM, 6 PM, etc.
                end_time = time(start_hour + index + 1, 0)  # Slot ends at 5 PM, 6 PM, 7 PM, etc.
                
                # Create a time slot for this age group, date, and time period
                time_slot = TimeSlot(
                    playground=playground,
                    date=current_date,
                    start_time=start_time,
                    end_time=end_time,
                    age_group=age_group,
                    max_positions=34,  # Set a default value for max_positions
                    available_positions=34,  # Initially, available positions will be equal to max_positions
                )
                time_slot.save()
                created_slots.append(time_slot)

            # Move to the next day
            current_date += timedelta(days=1)

        return Response({"message": "Time slots created successfully", "created_slots": len(created_slots)})
    

