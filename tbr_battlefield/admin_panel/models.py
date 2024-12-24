from django.db import models


class Playground(models.Model):
    name = models.CharField(max_length=100)  # Name of the playground
    location = models.TextField()  # Address or location of the playground
    facilities = models.TextField()  # Facilities available (e.g., "Restrooms, Parking, Snacks")
    playground_registration_start_date = models.DateField()
    playground_registration_end_date = models.DateField()

    def __str__(self):
        return self.name
    



# class TimeSlot(models.Model):
#     slot_time = models.CharField(max_length=100)
#     start_time = models.TimeField(null=False) 
#     end_time = models.TimeField(null=False) 
#     age_group_min = models.PositiveIntegerField(null=False) 
#     age_group_max = models.PositiveIntegerField(null=False) 
#     is_active = models.BooleanField(default=True)
#     total_positions = models.PositiveIntegerField(default=17)
#     max_users_per_position = models.PositiveIntegerField(default=2)
#     booked_positions = models.PositiveIntegerField(default=0)

#     def save(self, *args, **kwargs):
#         # Automatically mark slot as inactive if all positions are booked
#         if self.booked_positions >= self.total_positions * self.max_users_per_position:
#             self.is_active = False
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.start_time} - {self.end_time}"




# class Position(models.Model):
#     name = models.CharField(max_length=100)
#     time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name="positions")
#     current_bookings = models.PositiveIntegerField(default=0)
#     max_bookings = models.PositiveIntegerField(default=2)

#     class Meta:
#         unique_together = ('name', 'time_slot')    

#     @property
#     def is_available(self):
#         return self.current_bookings <= self.max_bookings

#     def book_position(self):
#         if self.is_available:
#             self.current_bookings += 1
#             self.save()
#         else:
#             raise ValueError(f"{self.name} is already fully booked for this slot.")
        
#     def __str__(self):
#         return f"{self.name} ({self.time_slot.start_time} - {self.time_slot.end_time})"
