from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsManagerOrAdmin
from .permissions import IsAdminOrOwner
from .serializers import TaskInputSerialier, TaskOutputSerializer
from .services import create_task, get_user_tasks
from rest_framework import generics
from .models import Task

class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin] #global RBAC
    
    def get(self, request):
        print("===== DEBUG: TaskListAPIView.get() called =====")
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        print("Groups:", list(request.user.groups.values_list('name', flat=True)))
        tasks = get_user_tasks(request.user) #service call
        serializer = TaskOutputSerializer(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        input_serializer = TaskInputSerialier(data=request.data)
        if input_serializer.is_valid():
            task = create_task(input_serializer.validated_data, request.user) #service call
            output_serializer = TaskOutputSerializer(task)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]  # module + object

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, obj)  # triggers object perm
        serializer = TaskOutputSerializer(obj)
        return Response(serializer.data)

