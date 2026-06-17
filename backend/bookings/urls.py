from django.urls import path

from .views import CreateBookingView, UserBookingListView, OpenMatchListView, OpenMatchDetailView, JoinOpenMatchView

urlpatterns = [
    path('my-bookings/', UserBookingListView.as_view()),
    path('new-booking/', CreateBookingView.as_view()),
    path('open-matches/', OpenMatchListView.as_view()),
    path('open-matches/<int:match_id>/', OpenMatchDetailView.as_view()),
    path('open-matches/<int:match_id>/join/', JoinOpenMatchView.as_view()),
]