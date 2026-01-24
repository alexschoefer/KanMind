from django.urls import path
from .views import BoardDashboardView

urlpatterns = [
    path('api/boards/', BoardDashboardView.as_view(), name="boardDashboard"),
]