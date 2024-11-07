"""
UserFacade provides high-level user operations, including creating, retrieving,
updating, and deleting users. This class acts as a service layer interfacing
with the user repository.
"""

from app.models.user import User
from email_validator import EmailNotValidError


class UserFacade():
    """
        Service class for managing user operations, including user creation,
        retrieval, updating, and deletion.
    """

    def __init__(self, selected_repo):
        """
        Initializes the UserFacade with a repository.

        Args:
            selected_repo: The repository instance to manage user persistence.
        """
        self.user_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_user(self, user_data):
        """
        Creates a new user.

        Args:
            user_data (dict): Dictionary containing user information including
                            'first_name', 'last_name', 'email', and 'password'.

        Returns:
            dict: The created user in dictionary form.

        Raises:
            ValueError: If a user with the same email already exists
            or if validation fails.
        """
        print(f"Creating user with data: {user_data}")

        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=False
        )
        new_user.hash_password(user_data["password"])

        existing_user = self.user_repo.get_by_attribute(
            "email", new_user.email)

        if existing_user:
            raise ValueError(
                f"User with email: {new_user.email} already exists.")

        if not new_user.is_valid():
            raise ValueError(
                "User validation failed. Please check the email "
                "and other attributes.")

        print(
            f"User {new_user.first_name} {new_user.last_name} "
            "passed validation.")

        self.user_repo.add(new_user)

        return new_user.to_dict()

    #   <------------------------------------------------------------------------>

    def get_user(self, user_id):
        """
        Retrieves a user by ID.

        Args:
            user_id (str): The unique identifier of the user.

        Returns:
            dict: The user data in dictionary form.

        Raises:
            ValueError: If the user is not found.
        """
        user = self.user_repo.get(user_id)

        if user:
            return user.to_dict()
        else:
            raise ValueError(f"User with id {user_id} not found.")

    #   <------------------------------------------------------------------------>

    def get_user_by_email(self, email):
        """
        Retrieves a user by email.

        Args:
            email (str): The email address of the user.

        Returns:
            User: The user object if found.

        Raises:
            ValueError: If the user is not found.
        """
        user = self.user_repo.get_by_attribute("email", email)

        if not user:
            raise ValueError("User not found")

        return user

    #   <------------------------------------------------------------------------>

    def get_all_users(self):
        """
        Retrieves all users.

        Returns:
            list: A list of all users in dictionary form.
        """
        users = self.user_repo.get_all()

        return [user.to_dict() for user in users]

    #   <------------------------------------------------------------------------>

    def update_user(self, user_id, new_data):
        """
        Updates a user's data.

        Args:
            user_id (str): The unique identifier of the user to update.
            new_data (dict): Dictionary with the updated user information.

        Returns:
            dict: The updated user data in dictionary form.

        Raises:
            ValueError: If the user is not found.
        """
        user = self.user_repo.get(user_id)

        if user:
            self.user_repo.update(user_id, new_data)

            return user.to_dict()

        else:
            raise ValueError(f"User with id {user_id} not found.")

    #   <------------------------------------------------------------------------>

    def delete_user(self, user_id):
        """
        Deletes a user by ID.

        Args:
            user_id (str): The unique identifier of the user to delete.

        Raises:
            ValueError: If the user is not found.
        """
        user = self.user_repo.get(user_id)

        if user:
            print(f"Deleted user: {user}")
            self.user_repo.delete(user_id)

        else:
            raise ValueError(f"User with id {user_id} not found.")
