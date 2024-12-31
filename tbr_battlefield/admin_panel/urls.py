from django.urls import path,include
from admin_panel.views import PlaygroundViewSet,AdminUserViewSet,AdminCoachViewSet ,TimeSlotAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("playground",PlaygroundViewSet , basename='playground')
router.register("admin_user", AdminUserViewSet , basename="manageuser")
router.register("admin_coach", AdminCoachViewSet , basename="managecoach")




urlpatterns = [

    # Time-Slot Api
    path('timeslot-create/', TimeSlotAPIView.as_view(), name='create_time_slots'),
    path('timeslot/', TimeSlotAPIView.as_view(), name='timeslot-crud'),  # For all operations
    path('timeslot/<int:id>/', TimeSlotAPIView.as_view(), name='timeslot-crud-detail'),  # For specific operations by ID

    path("",include(router.urls))

]
