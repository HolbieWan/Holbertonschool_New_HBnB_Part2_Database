from app import create_app
from app.extensions import db
from app.models.user import User

# Initialize the Flask application
app = create_app(config_name='default')

with app.app_context():

    superuser = User(
        first_name="Admin",
        last_name="Admin",
        email="admin@gmail.com",
        is_admin=True,
        password="adminpassword"
    )
    superuser.hash_password(superuser.password)

    db.session.add(superuser)
    db.session.commit()

    print("Superuser created successfully!")

# Creating super_user: run in root of repo: python3  create_super_user.py