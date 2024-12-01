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

    def test_valid_java_code(self):
        url = reverse('compile_code')
        data = {
            'code':'public class Main { public static void main(String[] args) {System.out.println("Hello, Java!");}}', 'language': 'java'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, Java!', response.json()['output'])
        
    def test_invalid_java_code(self):
        url = reverse('compile_code')
        data = {
            'code': 'public class Main { public static void main(String[] args) { System.out.println("Hello, Java!"}}','language': 'java'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error:', response.json()['output'])

    def test_valid_cpp_code(self):
        url = reverse('compile_code')
        data = {
            'code': '#include <iostream>\nusing namespace std;\nint main() { cout << "Hello, C++!" << endl; return 0; }', 'language': 'cpp'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, C++!', response.json()['output'])

    def test_invalid_cpp_code(self):
        url = reverse('compile_code') 
        data = { 'code': '#include <iostream>\nusing namespace std;\nint main() { cout << "Hello, C++!" << endl return 0; }', 'language': 'cpp' } 
        response = self.client.post(url, json.dumps(data), content_type='application/json') 
        self.assertEqual(response.status_code, 200) 
        self.assertIn('Error:', response.json()['output'])
        