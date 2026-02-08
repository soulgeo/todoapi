from rest_framework import serializers

from todos.models import Todo, TodoItem


class TodoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = (
            'id',
            'name',
            'todo',
            'is_complete',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'todo', 'created_at', 'updated_at')


class TodoSerializer(serializers.ModelSerializer):
    items = TodoItemSerializer(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = (
            'id',
            'name',
            'user',
            'description',
            'items',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
