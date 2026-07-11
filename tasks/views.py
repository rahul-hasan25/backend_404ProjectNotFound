from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from datetime import datetime

class TasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user       = request.user
        date_param = request.query_params.get('date', None)
        queryset   = Task.objects.filter(user=user)
        
        if date_param:
            try:
                parsed_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset    = queryset.filter(task_date=parsed_date)
            except ValueError:
                pass
        queryset = queryset.order_by('-created_at')

        todo_page        = request.query_params.get('todo_page', 1)
        in_progress_page = request.query_params.get('in_progress_page', 1)
        done_page        = request.query_params.get('done_page', 1)
        
        page_size = 2

        todo_queryset        = queryset.filter(status='todo')
        in_progress_queryset = queryset.filter(status='in_progress')
        done_queryset        = queryset.filter(status='done')

        todo_paginator        = Paginator(todo_queryset, page_size)
        in_progress_paginator = Paginator(in_progress_queryset, page_size)
        done_paginator        = Paginator(done_queryset, page_size)

        try:
            todo_data = todo_paginator.page(todo_page)
        except:
            todo_data = todo_paginator.page(1)

        try:
            in_progress_data = in_progress_paginator.page(in_progress_page)
        except:
            in_progress_data = in_progress_paginator.page(1)

        try:
            done_data = done_paginator.page(done_page)
        except:
            done_data = done_paginator.page(1)

        return Response({
            'todo': {
                'results'     : TaskSerializer(todo_data.object_list, many=True).data,
                'total_pages' : todo_paginator.num_pages,
                'current_page': todo_data.number,
                'total_count' : todo_queryset.count()
            },
            'in_progress': {
                'results'     : TaskSerializer(in_progress_data.object_list, many=True).data,
                'total_pages' : in_progress_paginator.num_pages,
                'current_page': in_progress_data.number,
                'total_count' : in_progress_queryset.count()
            },
            'done': {
                'results'     : TaskSerializer(done_data.object_list, many=True).data,
                'total_pages' : done_paginator.num_pages,
                'current_page': done_data.number,
                'total_count' : done_queryset.count()
            }
        })
        
    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class TasksDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            return None

    def patch(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'detail': 'Case study not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        if 'due_date' in data and data['due_date'] == "":
            data['due_date'] = None
            
        if 'task_date' in data and (data['task_date'] == "" or data['task_date'] is None):
            data['task_date'] = task.task_date
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            return Response({'detail': 'Case study not found.'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)