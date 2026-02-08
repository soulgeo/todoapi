from django.conf import settings
from django.db import models


class Todo(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='todos'
    )
    description = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class TodoItem(models.Model):
    name = models.CharField(max_length=255)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='items')
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
