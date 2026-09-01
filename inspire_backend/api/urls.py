from django.urls import path
from .views import (
    LeaderboardAPIView,
    UpdateScoresAPIView,
    ResetScoresAPIView,
    RegistrationCreateAPIView,
    RegistrationListAPIView,
    AdminLoginAPIView,
    EventListAPIView
)

urlpatterns = [
    # Live Leaderboard & Scores API
    path('scores/', LeaderboardAPIView.as_view(), name='scores-leaderboard'),
    path('scores/update/', UpdateScoresAPIView.as_view(), name='scores-update'),
    path('scores/reset/', ResetScoresAPIView.as_view(), name='scores-reset'),

    # Student Delegate Registrations API
    path('register/', RegistrationCreateAPIView.as_view(), name='register-delegate'),
    path('registrations/', RegistrationListAPIView.as_view(), name='registrations-list'),

    # Admin Authentication API
    path('admin/login/', AdminLoginAPIView.as_view(), name='admin-login'),

    # Competition Events Metadata API
    path('events/', EventListAPIView.as_view(), name='events-list'),
]
