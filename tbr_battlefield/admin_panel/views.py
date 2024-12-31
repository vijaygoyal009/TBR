from django.shortcuts import render
from rest_framework import viewsets
from admin_panel.serializers import PlaygroundSerializer , AdminUserSerializer , AdminCoachSerializer , TimeSlotSerializer
from admin_panel.models import Playground , TimeSlot , Position
from auth_app.permissions import IsAdminUser
from auth_app.models import CustomUser 
from rest_framework.response import Response
from datetime import timedelta, time
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status
from django.db import transaction, IntegrityError



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
                return Response({"error": "TimeSlot not found."}, status=404)
                
            return Response(TimeSlotSerializer(time_slot).data)

        time_slots = TimeSlot.objects.all()
        return Response(TimeSlotSerializer(time_slots, many=True).data)

    def post(self, request, *args, **kwargs):
        playground_id = request.data.get('playground_id')
        age_groups = request.data.get('age_group', [])  # e.g., ["0-8", "9-10", "11-12", ...]
        time_slot_duration = request.data.get('time_slot_duration', 60)  # Default 60 minutes per slot
        
        try:
            playground = Playground.objects.get(id=playground_id)
        except Playground.DoesNotExist:
            return Response({"error": "Playground not found."}, status=404)

        start_hour = 16  # 4 PM
        end_hour = 21  # 9 PM
        current_date = playground.playground_registration_start_date
        end_date = playground.playground_registration_end_date

        created_slots = 0
        existing_slots = 0

        # Define default roles and counts
        roles_with_counts = {
            "Left Fielder": 2,
            "Center Fielder": 2,
            "Shortstop": 2,
            "Third Baseman": 2,
            "Second Baseman": 2,
            "First Baseman": 2,
            "Pitcher": 4,
            "Base Runner": 2,
            "Right Fielder": 2,
            "Hitter": 10,
            "Catcher": 4,
        }

        # Loop through the entire date range
        while current_date <= end_date:
            if current_date.weekday() in [1, 2, 3]:  # Only create slots on Tuesday (1), Wednesday (2), Thursday (3)
                for index, age_group in enumerate(age_groups):
                    start_time = time(start_hour + index, 0)
                    end_time = time(start_hour + index + 1, 0)

                    # Check if this timeslot already exists
                    existing_slot = TimeSlot.objects.filter(
                        playground=playground,
                        date=current_date,
                        start_time=start_time,
                        end_time=end_time,
                        age_group=age_group
                    ).first()

                    if not existing_slot:  # Only create the slot if it doesn't already exist
                        try:
                            with transaction.atomic():  # Ensure atomicity for both time slot and positions creation
                                # Create the time slot
                                time_slot = TimeSlot.objects.create(
                                    playground=playground,
                                    date=current_date,
                                    start_time=start_time,
                                    end_time=end_time,
                                    age_group=age_group,
                                    max_positions=34,  # Set a default value for max_positions
                                    available_positions=34,  # Initially, available positions will be equal to max_positions
                                )

                                # Create positions for the time slot
                                for role, count in roles_with_counts.items():
                                    for _ in range(count):
                                        Position.objects.create(role=role, time_slot=time_slot)

                                created_slots += 1

                        except IntegrityError:
                            # This will happen if the time slot already exists, skip and increase existing slots count
                            existing_slots += 1

            current_date += timedelta(days=1)

        # Return response with a summary of created slots and skipped existing slots
        if created_slots > 0:
            return Response({
                "message": f"{created_slots} time slots created successfully with positions."
            })
        elif existing_slots > 0:
            return Response({
                "message": f"Time slots already exist for the selected date range. ({existing_slots} slots found)"
            })
        else:
            return Response({
                "message": "No time slots created."
            })



    # def put(self, request, *args, **kwargs):
    #     """
    #     Update a specific time slot
    #     """
    #     slot_id = kwargs.get('id')
    #     if not slot_id:
    #         return Response({"error": "TimeSlot ID is required for updating."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         time_slot = TimeSlot.objects.get(id=slot_id)
    #     except TimeSlot.DoesNotExist:
    #         return Response({"error": "TimeSlot not found."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = TimeSlotSerializer(time_slot, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"message": "Time slot updated successfully.", "time_slot": serializer.data})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, *args, **kwargs):
    #     """
    #     Delete a specific time slot
    #     """
    #     slot_id = kwargs.get('id')
    #     if not slot_id:
    #         return Response({"error": "TimeSlot ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         time_slot = TimeSlot.objects.get(id=slot_id)
    #         time_slot.delete()
    #         return Response({"message": "Time slot deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    #     except TimeSlot.DoesNotExist:
    #         return Response({"error": "TimeSlot not found."}, status=status.HTTP_404_NOT_FOUND)