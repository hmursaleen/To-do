from django.test import TestCase

# Create your tests here.
'''
class TestTodo(TestCase):
    def test_todo_list(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_todo_create(self):
        response = self.client.post('/api/todos/', {'title': 'Test Todo'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Todo')

    def test_todo_update(self):
        todo = Todo.objects.create(title='Test Todo')
        response = self.client.put('/api/todos/{}/'.format(todo.id), {'title': 'Updated Todo'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Todo')

    def test_todo_delete(self):
        todo = Todo.objects.create(title='Test Todo')
        response = self.client.delete('/api/todos/{}/'.format(todo.id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Todo.objects.count(), 0)
'''

