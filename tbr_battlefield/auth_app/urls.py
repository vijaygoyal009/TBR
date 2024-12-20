from django.urls import path
# from test_model.auth_user import views
from . import views


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("UserSignup/",views.UserSignupView.as_view() , name='usersignup'),
    path("CoachSignup/",views.CoachSignupView.as_view() , name='coachsignup'),
    path("AdminSignup/",views.AdminSignupView.as_view() , name='adminsignup'),


    # JWT Token Generation and Refresh URLs
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]