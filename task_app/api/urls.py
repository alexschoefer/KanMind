from django.urls import path
from .views import TasksAssignedToMeView, TasksReviewedToMeView, TaskCreateView, SingleTaskView, CommentListCreateAPIView

urlpatterns = [
    path('api/tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name="tasks-assigned-to-me"),
    path('api/tasks/reviewing/', TasksReviewedToMeView.as_view(), name="tasks-reviewed-to-me"),
    path('api/tasks/', TaskCreateView.as_view(), name="create-task"),
    path('api/tasks/<int:pk>/', SingleTaskView.as_view(), name="task"),
    path('api/tasks/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name="comment"),
]