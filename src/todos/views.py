from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Todo, TodoItem
from .serializers import TodoItemSerializer, TodoSerializer


def _bad_request(errors):
    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def _forbidden():
    return Response(
        {"error": "You do not have access to this resource."},
        status=status.HTTP_403_FORBIDDEN,
    )


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_todos(request):
    if request.method == 'GET':
        todos = Todo.objects.prefetch_related('items').filter(user=request.user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if not serializer.is_valid():
            return _bad_request(serializer.errors)

        serializer.save(user=request.user)
        return Response(
            {'message': 'Todo created successfully'}, status=status.HTTP_200_OK
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo(request, id):
    todo = Todo.objects.prefetch_related('items').get(id=id)
    if todo.user != request.user:
        return _forbidden()

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if not serializer.is_valid():
            return _bad_request(serializer.errors)

        serializer.save()
        return Response(
            {'message': 'Todo updated successfully'}, status=status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        todo.delete()
        return Response(
            {'message': 'Todo deleted successfully'}, status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo_item(request, id):
    todo = Todo.objects.get(id=id)
    if todo.user != request.user:
        return _forbidden()

    serializer = TodoItemSerializer(data=request.data)
    if not serializer.is_valid():
        return _bad_request(serializer.errors)

    serializer.save(todo=todo)
    return Response(
        {'message': 'Item created successfully'}, status=status.HTTP_200_OK
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_item(request, id, iid):
    todo = Todo.objects.get(id=id)
    if todo.user != request.user:
        return _forbidden()

    item = TodoItem.objects.get(id=iid)
    if item.todo != todo:
        error = {'error': 'The todo has no item matching the iid provided.'}
        return _bad_request(error)

    if request.method == 'GET':
        serializer = TodoItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = TodoItemSerializer(item, data=request.data)
        if not serializer.is_valid():
            return _bad_request(serializer.errors)

        serializer.save()
        return Response(
            {'message': 'Item updated successfully'}, status=status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        item.delete()
        return Response(
            {'message': 'Item deleted successfully'}, status=status.HTTP_200_OK
        )
