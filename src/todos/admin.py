from django.contrib import admin

from .models import Todo, TodoItem

class TodoItemInline(admin.TabularInline):
    model = TodoItem


class TodoAdmin(admin.ModelAdmin):
    inlines = [
        TodoItemInline
    ]

admin.site.register(Todo, TodoAdmin)
