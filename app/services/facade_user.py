from app.models.user import User
from email_validator import EmailNotValidError

class UserFacade():

    def __init__(self, selected_repo):
        self.user_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_user(self, user_data):
        print(f"Creating user with data: {user_data}")

        user = User(
            first_name=user_data["first_name"], 
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=user_data["is_admin"]
        )

        existing_user = self.user_repo.get_by_attribute("email", user.email)
        
        if existing_user:
            raise ValueError(f"User with email: {user.email} already exists.")

        if not user.is_valid():
            raise ValueError("User validation failed. Please check the email and other attributes.")

        print(f"User {user.first_name} {user.last_name} passed validation.")
        self.user_repo.add(user)
        return user.to_dict()

    #   <------------------------------------------------------------------------>

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            return user.to_dict()
        else:
            raise ValueError(f"User with id {user_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def get_user_by_attribute(self, attr):
        pass

    #   <------------------------------------------------------------------------>

    def get_all_users(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]

    #   <------------------------------------------------------------------------>

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update(user_id, new_data)
            return user.to_dict()
        else:
            raise ValueError(f"User with id {user_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            print(f"Deleted user: {user}")
            self.user_repo.delete(user_id)
        else:
            raise ValueError(f"User with id {user_id} not found.")
