import os
import sys
from dotenv import load_dotenv

# 1. Load environment variables from .env
load_dotenv()

# 2. Validate critical infrastructure
missing_vars = []
required_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"]

for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print(f"CRITICAL: Missing environment variables: {', '.join(missing_vars)}")
    print("Please check your .env file and ensure all required AWS credentials are set.")
    sys.exit(1) # Stop the script immediately

print("Environment validated. Starting orchestration...")

# Now proceed with your imports and logic...
from app.observers.aws_observer import AWSObserver
# ... rest of your code
