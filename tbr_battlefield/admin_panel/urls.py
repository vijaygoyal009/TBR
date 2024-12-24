from django.urls import path,include
from admin_panel.views import PlaygroundViewSet,AdminUserViewSet,AdminCoachViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("playground",PlaygroundViewSet , basename='playground')
router.register("admin_user", AdminUserViewSet , basename="manageuser")
router.register("admin_coach", AdminCoachViewSet , basename="managecoach")




urlpatterns = [

    path("",include(router.urls))

]