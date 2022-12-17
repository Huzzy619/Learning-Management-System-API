from rest_framework.test import APIClient
from rest_framework import status

class TestTasksCreation:

    def test_if_user_is_mentor(self):
        # Arrange
        # Act
        api = APIClient()

        response = api.post('/learn/task')
        # Assert

        assert response.status_code == status.HTTP_401_UNAUTHORIZED