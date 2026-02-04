from django.urls import path
from .views import BoardDashboardView, SingleBoardDetailView, EmailCheckView

urlpatterns = [
    path('api/boards/', BoardDashboardView.as_view(), name="boardDashboard"),
    path('api/boards/<int:pk>/', SingleBoardDetailView.as_view(), name="board-detail"),
    path('api/email-check/', EmailCheckView.as_view(), name="email-check")
]