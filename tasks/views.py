# tasks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import CanViewTask, CanMarkCompleted, CanManageTask
from .serializers import TaskInputSerializer, TaskOutputSerializer
from .services import create_task, get_user_tasks

class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewTask]  # everyone can list

    def get(self, request):
        tasks = get_user_tasks(request.user)
        serializer = TaskOutputSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Only managers can create
        if not request.user.groups.filter(name__in=['planning_head', 'cutting_supervisor']).exists():
            return Response({"detail": "You do not have permission to create tasks."}, status=403)
        
        input_serializer = TaskInputSerializer(data=request.data)
        if input_serializer.is_valid():
            task = create_task(input_serializer.validated_data, request.user)
            output_serializer = TaskOutputSerializer(task)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(input_serializer.errors, status=400)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, CanViewTask]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=404)
        serializer = TaskOutputSerializer(obj)
        return Response(serializer.data)

    def patch(self, request, pk):  # mark as completed
        obj = self.get_object(pk)
        if not obj:
            return Response(status=404)
        
        if not CanMarkCompleted().has_object_permission(request, self, obj):
            return Response({"detail": "You do not have permission to mark this task as completed."}, status=403)
        
        obj.completed = request.data.get('completed', obj.completed)
        obj.save()
        return Response(TaskOutputSerializer(obj).data)