from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/",include("auth_app.urls")),
    path("admin_panel/",include("admin_panel.urls"))
]
