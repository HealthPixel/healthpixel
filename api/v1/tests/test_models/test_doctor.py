import unittest
from unittest.mock import patch, MagicMock
from flask import url_for
from app import app


class TestDoctorViews(unittest.TestCase):

    def setUp(self):
        """Set up a test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('models.storage.all')
    def test_get_doctors(self, mock_storage_all):
        """Test retrieving all doctors."""
        doctor1 = MagicMock()
        doctor1.to_dict.return_value = {"id": "1", "name": "Doctor One"}
        doctor2 = MagicMock()
        doctor2.to_dict.return_value = {"id": "2", "name": "Doctor Two"}
        
        mock_storage_all.return_value = [doctor1, doctor2]

        response = self.app.get('/doctors')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {"id": "1", "name": "Doctor One"},
            {"id": "2", "name": "Doctor Two"}
        ])

    @patch('models.storage.get')
    def test_get_a_doctor_success(self, mock_storage_get):
        """Test retrieving a doctor by ID (success)."""
        doctor = MagicMock()
        doctor.to_dict.return_value = {"id": "1", "name": "Doctor One"}
        
        mock_storage_get.return_value = doctor

        response = self.app.get('/doctor/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": "1", "name": "Doctor One"})

    @patch('models.storage.get')
    def test_get_a_doctor_not_found(self, mock_storage_get):
        """Test retrieving a doctor by ID (doctor not found)."""
        mock_storage_get.return_value = None

        response = self.app.get('/doctor/1')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Doctor does not exist!", response.data)

    @patch('models.storage.get')
    @patch('flask_login.current_user')
    def test_update_a_doctor_not_authorized(self, mock_current_user, mock_storage_get):
        """Test update doctor when the current user is not a doctor."""
        mock_current_user.is_authenticated = True
        mock_current_user.return_value = MagicMock()
        mock_current_user.return_value.is_authenticated = True
        mock_current_user.return_value.is_doctor = False  # Simulate non-doctor user

        response = self.app.post('/doctor/1/update_doctor')
        self.assertEqual(response.status_code, 403)

    @patch('models.storage.get')
    @patch('flask_login.current_user')
    def test_update_a_doctor_success(self, mock_current_user, mock_storage_get):
        """Test update doctor when the current user is a doctor."""
        doctor = MagicMock()
        doctor.to_dict.return_value = {
            "id": "1", "first_name": "John", "last_name": "Doe",
            "email": "johndoe@example.com", "phone_number": "123456789",
            "specialization": "Cardiology"
        }

        mock_current_user.is_authenticated = True
        mock_current_user.return_value = doctor
        mock_storage_get.return_value = doctor

        response = self.app.post('/doctor/1/update_doctor', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'phone_number': '123456789',
            'specialization': 'Cardiology',
            'password': 'password123',
            'conf_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success

    @patch('models.storage.get')
    def test_delete_a_doctor_success(self, mock_storage_get):
        """Test successfully deleting a doctor."""
        doctor = MagicMock()
        mock_storage_get.return_value = doctor

        response = self.app.delete('/doctor/1')
        self.assertEqual(response.status_code, 200)

    @patch('models.storage.get')
    def test_delete_a_doctor_not_found(self, mock_storage_get):
        """Test deleting a doctor that does not exist."""
        mock_storage_get.return_value = None

        response = self.app.delete('/doctor/1')
        self.assertEqual(response.status_code, 404)

    @patch('models.storage.query')
    @patch('flask_login.current_user')
    def test_register_patient_already_exists(self, mock_current_user, mock_storage_query):
        """Test registering a patient that already exists."""
        mock_current_user.is_authenticated = True
        mock_current_user.return_value.is_doctor = True  # Simulate doctor user
        
        existing_patient = MagicMock()
        mock_storage_query.return_value.filter_by.return_value.first.return_value = existing_patient

        response = self.app.post('/doctor/register-patient', data={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'janedoe@example.com',
            'phone_number': '987654321',
            'password': 'password123',
            'conf_password': 'password123',
            'date_of_birth': '1990-01-01',
            'gender': 'Female',
            'address': '1234 Elm St',
            'zipcode': '10001',
            'blood_group': 'O+',
            'emg_contact_name': 'Emergency Contact',
            'emg_contact_phone': '123456789'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Patient already exists', response.data)


if __name__ == '__main__':
    unittest.main()
