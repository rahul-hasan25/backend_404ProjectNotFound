from django.urls import path
from .views import TasksAPIView, TasksDetailAPIView


urlpatterns = [
    path('tasks/', TasksAPIView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TasksDetailAPIView.as_view(), name='task-detail'),
]