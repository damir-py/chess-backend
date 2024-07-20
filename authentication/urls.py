from django.urls import path

from .views import AuthenticationAPIView

urlpatterns = [
    path('authentication/register/', AuthenticationAPIView.as_view({'post': 'register'}), name='register'),
    path('authentication/verify/', AuthenticationAPIView.as_view({'post': 'verify'}), name='verify'),
    path('authentication/login/', AuthenticationAPIView.as_view({'post': 'login'}), name='login'),
]