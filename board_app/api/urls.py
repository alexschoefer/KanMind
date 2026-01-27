from django.urls import path
from .views import BoardDashboardView, SingleBoardDetailView

urlpatterns = [
    path('api/boards/', BoardDashboardView.as_view(), name="boardDashboard"),
    path('api/boards/<int:pk>/', SingleBoardDetailView.as_view(), name="board-detail")
]