# Example for Python
import os
from langfuse import Langfuse

from dotenv import load_dotenv
load_dotenv()

langfuse = Langfuse(
    host="http://localhost:3000",
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
)

# Verify connection
if langfuse.auth_check():
    print("Langfuse client is authenticated and ready!")
else:
    print("Authentication failed. Please check your credentials and host.")


