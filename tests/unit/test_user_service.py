import unittest
from unittest.mock import MagicMock, patch
from login_api.services.user_service import UserService
from login_api.models.user_model import User
from login_api.error_handler.user_exceptions import UserAlreadyExistsError

class TestUserService(unittest.TestCase):

    def setUp(self):
        """Setup run before each test"""
        self.mock_repo = MagicMock()
        
        # Configure app context patch
        self.app_context_patch = patch('flask.current_app')
        self.mock_app = self.app_context_patch.start()
        
        # Initialize service
        self.user_service = UserService(self.mock_repo)
        
        # Sample test user
        self.test_user = User(
            id=1,
            email="test@example.com",
            password_hash="hashed_password",
            first_name="Test",
            last_name="User"
        )

    def tearDown(self):
        self.app_context_patch.stop()

    # Test Cases

    def test_create_user_success(self):
        """Test user creation"""
        # Arrange
        # Configure the mock to return test_user as the created user
        mock_user = MagicMock(spec=User)
        mock_user.id = 1
        mock_user.email = "test@example.com"
        mock_user.first_name = "Test"
        mock_user.last_name = "User"
        mock_user.is_active = True
        mock_user.created_at = "2025-07-06T13:31:12.923013"
        mock_user.updated_at = "2025-07-06T13:31:12.923023"
        mock_user.to_dict.return_value = {
            # "message": "User created successfully",
            # "user": {
                "id": 1,
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "is_active": True,
                "created_at": "2025-07-06T13:31:12.923013",
                "updated_at": "2025-07-06T13:31:12.923023"
            # }
	    }
        self.mock_repo.create.return_value = mock_user
        # Configure the mock to return None for email check (user doesn't exist)
        self.mock_repo.get_by_email.return_value = None
        
        # Act
        result = self.user_service.create_user(
            email="new@example.com",
            password="secure123",
            first_name="New",
            last_name="User",
            is_active=True
        )
        # Debug print (THIS IS CRUCIAL)
        print("\n=== IN TEST ===")
        print("Mock user:", mock_user)
        print("to_dict return:", mock_user.to_dict.return_value)
        print("Actual result:", result)
        print("Type of result:", type(result))
        
        # Assert
        self.assertEqual(result["message"], "User created successfully")
        # self.assertEqual(result["email"], "test@example.com")
        # Verify the mock interactions
        self.mock_repo.get_by_email.assert_called_once_with("new@example.com")
        self.mock_repo.create.assert_called_once()
        mock_user.to_dict.assert_called_once()

    # def test_create_user_duplicate_email(self):
    #     """Test creation fails with existing email"""
    #     # Setup mock - user already exists
    #     self.mock_repo.get_by_email.return_value = self.test_user
        
    #     # Verify exception is raised
    #     with self.assertRaises(UserAlreadyExistsError):
    #         self.user_service.create_user(
    #             email="existing@example.com",
    #             password="any",
    #             first_name="Existing",
    #             last_name="User",
    #             is_active=True
    #         )
        
    #     # Verify create was NOT called
    #     self.mock_repo.create.assert_not_called()

if __name__ == '__main__':
    unittest.main()