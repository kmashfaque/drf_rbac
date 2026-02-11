from django.urls import path
from .views import TaskDetailAPIView, TaskListAPIView

urlpatterns = [
    path('', TaskListAPIView.as_view()),
    path('<int:pk>/', TaskDetailAPIView.as_view())
]