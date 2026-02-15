from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_todos, name='list_todos'),
    path('<int:id>/', views.todo, name='todo'),
    path('<int:id>/items/', views.create_todo_item, name='create_todo_item'),
    path('<int:id>/items/<int:iid>/', views.todo_item, name='todo_item'),
]
