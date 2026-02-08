from django.urls import path

from . import views

urlpattens = [
    path('todos', views.list_todos),
    path('todos/<int:id>', views.todo),
    path('todos/<int:id>/items', views.create_todo_item),
    path('todos/<int:id>/items/<int:iid>', views.todo_item),
]
