"""
Test script for Google Sheets API connection
Run this script to check if your API connection works properly
"""

import requests
import os
from dotenv import load_dotenv
import json
import webbrowser

# Load environment variables from .env file
load_dotenv()

# Get API key and spreadsheet ID from environment variables
API_KEY = os.getenv("GOOGLE_SHEETS_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE_NAME = "A1:G100"  # Remove sheet name to get the default sheet

def get_sheet_names():
    """Get a list of sheet names in the spreadsheet"""
    if not API_KEY or not SPREADSHEET_ID:
        return []
    
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}?key={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        
        data = response.json()
        sheets = data.get('sheets', [])
        return [sheet['properties']['title'] for sheet in sheets]
    except Exception:
        return []

def test_api_connection():
    """Test the Google Sheets API connection and print detailed results"""
    # Check if API key and spreadsheet ID are available
    if not API_KEY:
        print("ERROR: GOOGLE_SHEETS_API_KEY not found in environment variables")
        print("Make sure you have a .env file with GOOGLE_SHEETS_API_KEY=your_api_key")
        return False
    
    if not SPREADSHEET_ID:
        print("ERROR: SPREADSHEET_ID not found in environment variables")
        print("Make sure you have a .env file with SPREADSHEET_ID=your_spreadsheet_id")
        return False
    
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:] if API_KEY else ''}")
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    
    # First get the available sheet names
    print("Fetching sheet names...")
    sheet_names = get_sheet_names()
    
    if not sheet_names:
        print("Could not retrieve sheet names. Trying with default sheet...")
        full_range = RANGE_NAME
    else:
        print(f"Available sheets: {', '.join(sheet_names)}")
        # Use the first sheet name
        full_range = f"{sheet_names[0]}!{RANGE_NAME}"
        print(f"Using sheet: {sheet_names[0]}")
    
    # Call the Sheets API
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{full_range}?key={API_KEY}"
    print(f"\nSending request to: {url}")
    
    try:
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")
        
        if response.status_code != 200:
            print("ERROR: API request failed")
            print(f"Response content: {response.text}")
            
            # Special handling for permission error
            if response.status_code == 403 and "PERMISSION_DENIED" in response.text:
                print("\n======= PERMISSION ERROR DETECTED =======")
                print("The API key doesn't have permission to access this spreadsheet.")
                print("\nTo fix this issue, you need to make your spreadsheet publicly accessible:")
                print("1. Open your spreadsheet in Google Sheets")
                print("2. Click 'Share' button in the top right")
                print("3. Click 'Change to anyone with the link'")
                print("4. Make sure 'Viewer' is selected")
                print("5. Click 'Done'")
                
                # Offer to open the spreadsheet
                share_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
                print(f"\nWould you like to open your spreadsheet now? Y/N")
                choice = input().strip().lower()
                if choice == 'y':
                    print(f"Opening: {share_url}")
                    webbrowser.open(share_url)
            elif response.status_code == 400 and "Unable to parse range" in response.text:
                print("\n======= SHEET NAME ERROR DETECTED =======")
                print("The sheet name in your range doesn't exist in the spreadsheet.")
                
                # Offer to open the spreadsheet so they can see the actual sheet names
                share_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
                print(f"\nWould you like to open your spreadsheet to check sheet names? Y/N")
                choice = input().strip().lower()
                if choice == 'y':
                    print(f"Opening: {share_url}")
                    webbrowser.open(share_url)
                    
                print("\nAfter checking the sheet name, update your .env file with:")
                print("SHEET_NAME=YourActualSheetName")
                
            return False
        
        # Parse the response
        result = response.json()
        
        if 'values' not in result:
            print("ERROR: No 'values' found in the API response")
            print(f"Response structure: {json.dumps(result, indent=2)}")
            return False
        
        values = result.get('values', [])
        if not values:
            print("ERROR: 'values' is empty")
            return False
        
        # Success!
        print(f"\nAPI test SUCCESSFUL!")
        print(f"Found {len(values)-1} data rows")
        print(f"Headers: {values[0]}")
        print(f"First data row: {values[1] if len(values) > 1 else 'No data rows found'}")
        
        # Save the successful sheet name to environment
        if sheet_names:
            print(f"\nTo use this sheet directly in your .env file, add:")
            print(f"SHEET_NAME={sheet_names[0]}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: Exception occurred: {str(e)}")
        return False

# This is the part that ensures the function actually runs
if __name__ == "__main__":
    print("Testing Google Sheets API connection...\n")
    test_result = test_api_connection()
    if not test_result:
        print("\nAPI test FAILED. Check the errors above.")
    
    # Let's also check if the .env file exists
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        print("\nWARNING: No .env file found in the current directory!")
        print(f"Expected location: {env_path}")
        print("Create a .env file with your credentials:")
        print("GOOGLE_SHEETS_API_KEY=your_api_key_here")
        print("SPREADSHEET_ID=your_spreadsheet_id_here")
        print("SHEET_NAME=your_sheet_name")
