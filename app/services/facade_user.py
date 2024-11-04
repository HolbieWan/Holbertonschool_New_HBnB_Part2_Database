from app.models.user import User
from email_validator import EmailNotValidError

class UserFacade():

    def __init__(self, selected_repo):
        self.user_repo = selected_repo

    # <------------------------------------------------------------------------>

    def create_user(self, user_data):
        print(f"Creating user with data: {user_data}")

        new_user = User(
            first_name=user_data["first_name"], 
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=False
        )
        new_user.hash_password(user_data["password"])

        existing_user = self.user_repo.get_by_attribute("email", new_user.email)
        
        if existing_user:
            raise ValueError(f"User with email: {new_user.email} already exists.")

        if not new_user.is_valid():
            raise ValueError("User validation failed. Please check the email and other attributes.")

        print(f"User {new_user.first_name} {new_user.last_name} passed validation.")
        self.user_repo.add(new_user)
        return new_user.to_dict()

    #   <------------------------------------------------------------------------>

    def get_user(self, user_id):
        user = self.user_repo.get(user_id)
        if user:
            return user.to_dict()
        else:
            raise ValueError(f"User with id {user_id} not found.")
        
    #   <------------------------------------------------------------------------>

    def get_user_by_email(self, email):
        users = self.user_repo.get_by_attribute("email", email)

        if not users:
            raise ValueError("User not found")
        if len(users) > 1:
            raise ValueError("Multiple users found with the same email")
        
        return users[0] 

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
