from django.contrib import admin
from admin_panel.models import Playground, TimeSlot

@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):        
    list_display = ['name' , 'location','facilities','playground_registration_start_date','playground_registration_end_date']



@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'playground', 'date', 'start_time', 'end_time', 'age_group', 'is_active']