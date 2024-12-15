import unittest
import json
from app import app, DB_FILE

class ZooManagementTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and sample database."""
        self.app = app.test_client()
        self.app.testing = True
        
 
        self.sample_db = {
            "employees": [
                {"id": 1, "name": "Alice", "position": "Caretaker"},
                {"id": 2, "name": "Bob", "position": "Manager"}
            ],
            "animals": [
                {"id": 1, "species": "Lion", "name": "Simba", "age": 3},
                {"id": 2, "species": "Elephant", "name": "Dumbo", "age": 7}
            ]
        }
        with open(DB_FILE, 'w') as file:
            json.dump(self.sample_db, file, indent=4)

    def tearDown(self):
        """Clean up test data after tests."""
        with open(DB_FILE, 'w') as file:
            file.write(json.dumps({"employees": [], "animals": []}))

    # ================= TEST EMPLOYEES ENDPOINT ================= #
    def test_get_employees(self):
        response = self.app.get('/employees')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_add_employees(self):
        new_employees = [
            {"name": "Charlie", "position": "Veterinarian"},
            {"name": "Diana", "position": "Trainer"}
        ]
        response = self.app.post('/employees', data=json.dumps(new_employees), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Charlie")

    def test_update_employees(self):
        updated_employees = [{"id": 1, "name": "Alice Updated", "position": "Head Caretaker"}]
        response = self.app.put('/employees', data=json.dumps(updated_employees), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[0]['name'], "Alice Updated")

    def test_delete_employees(self):
        response = self.app.delete('/employees', data=json.dumps([1]), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        response_after = self.app.get('/employees')
        data = json.loads(response_after.data)
        self.assertEqual(len(data), 1)

    # ================= TEST ANIMALS ENDPOINT ================= #
    def test_get_animals(self):
        response = self.app.get('/animals')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

    def test_add_animals(self):
        new_animals = [
            {"species": "Tiger", "name": "Shera", "age": 5}
        ]
        response = self.app.post('/animals', data=json.dumps(new_animals), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data[0]['name'], "Shera")

    def test_update_animals(self):
        updated_animals = [{"id": 1, "name": "Simba Updated", "age": 4}]
        response = self.app.put('/animals', data=json.dumps(updated_animals), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[0]['name'], "Simba Updated")

    def test_delete_animals(self):
        response = self.app.delete('/animals', data=json.dumps([1]), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        response_after = self.app.get('/animals')
        data = json.loads(response_after.data)
        self.assertEqual(len(data), 1)

if __name__ == '__main__':
    unittest.main()
