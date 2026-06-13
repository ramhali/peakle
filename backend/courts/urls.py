from django.urls import path

from .views import CourtListView, CourtCreateView, CourtDetailView

urlpatterns = [
    path('', CourtListView.as_view()),
    path('new/', CourtCreateView.as_view()),
    path('<int:court_id>/', CourtDetailView.as_view()),
]