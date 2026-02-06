# Django imports
from django.urls import path

# Local Imports
from .views import TasksAssignedToMeView, TasksReviewedToMeView, TaskCreateView, SingleTaskView, CommentListCreateAPIView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('api/tasks/assigned-to-me/', TasksAssignedToMeView.as_view(), name="tasks-assigned-to-me"), #View to show all tasks which are assigned to me
    path('api/tasks/reviewing/', TasksReviewedToMeView.as_view(), name="tasks-reviewed-to-me"), #View to show all tasks which are reviewing through me
    path('api/tasks/', TaskCreateView.as_view(), name="create-task"), #View to create a task for a board
    path('api/tasks/<int:pk>/', SingleTaskView.as_view(), name="task"), #View to update or delete a task at a board
    path('api/tasks/<int:pk>/comments/', CommentListCreateAPIView.as_view(), name="comment-collection"), #View to get or create a comment on a special task pk=task_id
    path('api/tasks/<int:task_id>/comments/<int:pk>', CommentRetrieveUpdateDestroyView.as_view(), name="comment") #View for deleting a comment on a special task pk=task_id
]