from django.contrib import admin
from auth_app.models import CustomUser , AdminProfile , UserProfile , CoachProfile


admin.site.register(CustomUser)
admin.site.register(AdminProfile)
admin.site.register(UserProfile)
admin.site.register(CoachProfile)

