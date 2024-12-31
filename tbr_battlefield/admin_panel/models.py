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
    max_positions = models.IntegerField(default=34)
    available_positions = models.IntegerField(default=34)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('playground', 'date', 'start_time', 'end_time', 'age_group')  # Prevent duplicate slots

    def create_default_positions(self):
        """Create default positions for this time slot."""
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
        for role, count in roles_with_counts.items():
            for _ in range(count):
                Position.objects.create(role=role, time_slot=self)

    def __str__(self):
        return f"{self.playground.name} - {self.date} ({self.start_time}-{self.end_time}, {self.age_group})"




class Position(models.Model):
    ROLE_CHOICES = [
        ("Left Fielder", "Left Fielder"),
        ("Center Fielder", "Center Fielder"),
        ("Shortstop", "Shortstop"),
        ("Third Baseman", "Third Baseman"),
        ("Second Baseman", "Second Baseman"),
        ("First Baseman", "First Baseman"),
        ("Pitcher", "Pitcher"),
        ("Base Runner", "Base Runner"),
        ("Right Fielder", "Right Fielder"),
        ("Hitter", "Hitter"),
        ("Catcher", "Catcher"),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_booked = models.BooleanField(default=False)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return f"{self.role} - {'Booked' if self.is_booked else 'Available'}"
