import unittest
import json
from app import app

class TestSensorLogAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_latest_sensor_log(self):
        response = self.app.get('/view/latest/sensor/data/public/?unique_id=3R6HuuiV')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('latest_log', data)

    def test_get_latest_sensor_log_missing_param(self):
        response = self.app.get('/view/latest/sensor/data/public/')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_get_latest_sensor_log_not_found(self):
        response = self.app.get('/view/latest/sensor/data/public/?unique_id=nonexistent_id')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
