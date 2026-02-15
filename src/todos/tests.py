from typing import cast

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Todo


class TodoAPITestCase(APITestCase):
    def setUp(self):
        self.username = 'foo'
        self.email = 'foo@bar.com'
        self.password = 'bar'
        self.todo_name = "test_todo"
        self.todo_description = "lorem ipsum"

        self.user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        self.todo = Todo.objects.create(
            name=self.todo_name,
            user=self.user,
            description=self.todo_description,
        )

        self.list_todos_url = reverse('list_todos')
        self.todo_url = reverse('todo', kwargs={'id': self.todo.pk})

    def test_unauthorized_list_todos(self):
        response = self.client.get(self.list_todos_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_create_todo(self):
        data = {'name': 'name', 'description': 'description'}
        response = self.client.post(self.list_todos_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_get_todo(self):
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_update_todo(self):
        data = {'name': 'new_name', 'description': 'new_description'}
        response = self.client.put(self.todo_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, self.todo_name)
        self.assertEqual(self.todo.description, self.todo_description)

    def test_unauthorized_delete_todo(self):
        response = self.client.delete(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Todo.objects.filter(id=self.todo.pk).exists())

    def test_other_user_cannot_get_todo_of_user(self):
        other_user = User.objects.create_user(
            username="bar", email="bar@foo.com", password="foo"
        )
        self.client.force_login(other_user)

        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_cannot_update_todo_of_user(self):
        other_user = User.objects.create_user(
            username="bar", email="bar@foo.com", password="foo"
        )
        self.client.force_login(other_user)

        data = {'name': 'new_name', 'description': 'new_description'}
        response = self.client.put(self.todo_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, self.todo_name)
        self.assertEqual(self.todo.description, self.todo_description)

    def test_other_user_cannot_delete_todo_of_user(self):
        other_user = User.objects.create_user(
            username="bar", email="bar@foo.com", password="foo"
        )
        self.client.force_login(other_user)

        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Todo.objects.filter(id=self.todo.pk).exists())

    def test_user_list_todos(self):
        todo2 = Todo.objects.create(
            name="todo2", user=self.user, description="desc2"
        )
        todo3 = Todo.objects.create(
            name="todo3", user=self.user, description="desc3"
        )

        other_user = User.objects.create_user(
            username="other", email="other@test.com", password="pwd"
        )
        Todo.objects.create(
            name="other_todo", user=other_user, description="other_desc"
        )

        self.client.force_login(self.user)
        response = cast(Response, self.client.get(self.list_todos_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        assert response.data is not None
        self.assertEqual(len(response.data), 3)

        # Verify the IDs match our user's todos
        returned_ids = {item['id'] for item in response.data}
        expected_ids = {self.todo.pk, todo2.pk, todo3.pk}
        self.assertEqual(returned_ids, expected_ids)

    def test_user_create_todo(self):
        self.client.force_login(self.user)

        data = {'name': 'name', 'description': 'description'}
        response = cast(
            Response, self.client.post(self.list_todos_url, data=data)
        )

        assert response.data is not None
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Todo.objects.filter(id=response.data['id']).exists())

    def test_user_get_todo(self):
        self.client.force_login(self.user)
        response = cast(Response, self.client.get(self.todo_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        assert response.data is not None
        self.assertEqual(response.data['name'], self.todo.name)
        self.assertEqual(response.data['description'], self.todo.description)

    def test_user_update_todo(self):
        self.client.force_login(self.user)

        data = {'name': 'new_name', 'description': 'new_description'}
        response = self.client.put(self.todo_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.todo.refresh_from_db()
        self.assertEqual(self.todo.name, 'new_name')
        self.assertEqual(self.todo.description, 'new_description')

    def test_user_delete_todo(self):
        self.client.force_login(self.user)
        response = cast(Response, self.client.delete(self.todo_url))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Todo.objects.filter(id=self.todo.pk).exists())
