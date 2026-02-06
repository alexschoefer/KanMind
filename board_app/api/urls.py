# Django imports
from django.urls import path

# Local Imports
from .views import BoardDashboardView, SingleBoardDetailView, EmailCheckView

urlpatterns = [
    path('api/boards/', BoardDashboardView.as_view(), name="boardDashboard"), #View to show all existing boards
    path('api/boards/<int:pk>/', SingleBoardDetailView.as_view(), name="board-detail"), #View to show special existing boards; pk = id of the special board
    path('api/email-check/', EmailCheckView.as_view(), name="email-check") #View to check a email adress
]