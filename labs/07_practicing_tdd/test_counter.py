"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app


class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        response = self.client.post("/counters/foo")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        response = self.client.post("/counters/bar")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post("/counters/bar")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """Test updating a counter"""
        response = self.client.post("/counters/baz")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        initial_count = response.get_json()["baz"]
        # Update the counter
        response = self.client.put("/counters/baz")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = response.get_json()["baz"]
        self.assertEqual(count, initial_count + 1)

    def test_read_a_counter(self):
        """It should read the counter"""
        response = self.client.post("/counters/bin")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Read the counter
        response = self.client.get("/counters/bin")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        count = response.get_json()["bin"]
        self.assertEqual(count, 0)

    def test_delete_a_counter(self):
        """It should delete the counter"""
        response = self.client.post("/counters/fob")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Delete the counter
        response = self.client.delete("/counters/fob")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.delete("/counters/fob")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
