from flask.cli import FlaskGroup
from app import create_app
from app.extensions import db
from app.models.user import User

def create_my_app():
    """Factory function to create the Flask app."""
    return create_app(config_name='default')

# Pass the factory function using `create_app` keyword argument
cli = FlaskGroup(create_app=create_my_app)

@cli.command("create_superuser")
def create_superuser():
    """Create a superuser with admin rights."""
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")
    password = input("Password: ")

    if User.query.filter_by(email=email).first():
        print("Error: A user with this email already exists.")
        return

    superuser = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_admin=True,
        password=password
    )
    superuser.hash_password(password)
    db.session.add(superuser)
    db.session.commit()

    print(f"Superuser {email} created successfully.")

if __name__ == "__main__":
    cli()

# To create super_user with CLI run: python3 manage.py create_superuser