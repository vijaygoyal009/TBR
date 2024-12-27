from django.db import models


class Playground(models.Model):
    name = models.CharField(max_length=100)  # Name of the playground
    location = models.TextField()  # Address or location of the playground
    facilities = models.TextField()  # Facilities available (e.g., "Restrooms, Parking, Snacks")
    playground_registration_start_date = models.DateField()
    playground_registration_end_date = models.DateField()

    def __str__(self):
        return self.name
    



class TimeSlot(models.Model):
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    age_group = models.CharField(max_length=20)  # Example: "6-10"
    max_positions = models.IntegerField(default=34)  # Default number of positions
    available_positions = models.IntegerField(default=34)  # Initially, all positions are available
    is_active = models.BooleanField(default=True)  # Slot is active by default

    def __str__(self):
        return f"{self.playground.name} - {self.date} ({self.start_time}-{self.end_time}, {self.age_group})"

    def save(self, *args, **kwargs):
        if self.max_positions is None:
            self.max_positions = 34  # Set a default value for max_positions
        if self.available_positions is None:
            self.available_positions = self.max_positions  # Default to max positions initially
        super(TimeSlot, self).save(*args, **kwargs)

    def book_position(self):
        if self.available_positions > 0:
            self.available_positions -= 1
            if self.available_positions == 0:
                self.is_active = False  # Deactivate the slot when no positions are available
            self.save()
        else:
            raise ValueError("No available positions left for this slot.")
