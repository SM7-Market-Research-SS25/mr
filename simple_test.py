"""
Very simple test script to check environment variables
"""

import os
from dotenv import load_dotenv

print("Starting simple test...")

# Check if .env file exists
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    print(f".env file found at: {env_path}")
else:
    print(f"ERROR: No .env file found at: {env_path}")

# Try to load environment variables
print("Trying to load environment variables...")
load_dotenv()

# Check if variables exist
api_key = os.getenv("GOOGLE_SHEETS_API_KEY")
spreadsheet_id = os.getenv("SPREADSHEET_ID")

print(f"GOOGLE_SHEETS_API_KEY exists: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API Key starts with: {api_key[:5]}")

print(f"SPREADSHEET_ID exists: {'Yes' if spreadsheet_id else 'No'}")
if spreadsheet_id:
    print(f"Spreadsheet ID: {spreadsheet_id}")

print("Simple test completed.")
