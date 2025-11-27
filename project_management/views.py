from rest_framework import viewsets
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
	queryset = Project.objects.all().order_by('name')
	serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
	queryset = Task.objects.all().order_by('due_date')
	serializer_class = TaskSerializer
