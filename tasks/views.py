# tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import CanViewTask, CanMarkCompleted, CanManageTask, IsAdminOrOwner
from .serializers import TaskInputSerialier, TaskOutputSerializer
from .services import create_task, get_user_tasks
from .models import Task
from accounts.permissions import IsManagerOrAdmin  # if you still use it

class TaskListAPIView(APIView):
    """
    List all tasks (filtered by user permissions) or create new task.
    """
    permission_classes = [IsAuthenticated, CanViewTask]

    def get(self, request):
        tasks = get_user_tasks(request.user)
        serializer = TaskOutputSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only certain roles can create tasks
        if not CanManageTask().has_permission(request, self):
            return Response(
                {"detail": "You do not have permission to create tasks."},
                status=status.HTTP_403_FORBIDDEN
            )

        input_serializer = TaskInputSerialier(data=request.data)
        if input_serializer.is_valid():
            task = create_task(input_serializer.validated_data, request.user)
            output_serializer = TaskOutputSerializer(task)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailAPIView(APIView):
    """
    Retrieve, update (mark completed), or delete a task.
    """
    permission_classes = [IsAuthenticated, CanViewTask]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskOutputSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Only allow marking as completed if permitted
        if not CanMarkCompleted().has_object_permission(request, self, obj):
            return Response(
                {"detail": "You do not have permission to mark this task as completed."},
                status=status.HTTP_403_FORBIDDEN
            )

        obj.completed = request.data.get('completed', obj.completed)
        obj.save(update_fields=['completed'])
        return Response(TaskOutputSerializer(obj).data)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Only managers can delete
        if not CanManageTask().has_permission(request, self):
            return Response(
                {"detail": "You do not have permission to delete tasks."},
                status=status.HTTP_403_FORBIDDEN
            )

        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)