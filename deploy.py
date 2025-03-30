from config.db import engine, Base
from models import User
import logging

# Set up logging to show SQLAlchemy SQL queries
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Print a message before attempting to create tables to confirm script execution
print("Attempting to create tables...")

try:
    # Attempt to create the table
    User.__table__.create(bind=engine)  # This should create the table
    print("✅ Tables created!")

    # Optionally, print the User model to verify it's imported correctly
    print("User model:", User)

except Exception as e:
    # If there’s an error during table creation, it will print here
    print(f"❌ Error creating tables: {str(e)}")
