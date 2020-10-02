from django.urls import path
from .views import UserLogin, userSignup, activateAccount, UserProfile

urlpatterns = [
    path('rest-auth/login', UserLogin.as_view()),
    path('signup/', userSignup, name='signup'),
    path('profile/<int:pk>/', UserProfile.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', activateAccount, name='activate'),
]