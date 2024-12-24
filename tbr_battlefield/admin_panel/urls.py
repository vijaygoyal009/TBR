from django.urls import path,include
from admin_panel.views import PlaygroundViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("playground",PlaygroundViewSet , basename='playground')



urlpatterns = [

    path("",include(router.urls))

]