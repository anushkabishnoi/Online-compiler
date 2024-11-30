from django.test import TestCase
from django.urls import reverse
import json 

# Create your tests here.
class CompileCodeTests(TestCase):
    def test_valid_python_code(self):
        url = reverse('compile_code')
        data = {'code': 'print("Hello, World!")', 'language': 'python'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, World!', response.json()['output'])

    def test_invalid_python_code(self):
        url = reverse('compile_code')
        data = {'code': 'print("Hello, World!"', 'language': 'python'}
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error:', response.json()['output'])