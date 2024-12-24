from django.contrib import admin
from admin_panel.models import Playground

@admin.register(Playground)
class PlaygroundAdmin(admin.ModelAdmin):        
    list_display = ['name' , 'location','facilities','playground_registration_start_date','playground_registration_end_date']