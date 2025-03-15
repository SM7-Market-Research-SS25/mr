"""
Script to inspect data from Google Sheets to identify data format issues
"""

import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import re

# Load environment variables
load_dotenv()

# Get API key, spreadsheet ID, and sheet name
API_KEY = os.getenv("GOOGLE_SHEETS_API_KEY")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME", "")

def get_sheet_names():
    """Get all sheet names from the spreadsheet"""
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
    except Exception as e:
        print(f"Error getting sheet names: {str(e)}")
        return []

def add_year_to_dates(date_str, year=None):
    """Add a year to date strings like 'Jan. 11'"""
    if not year:
        year = datetime.now().year
        
    # Handle abbreviated month names with dots
    if re.match(r'[A-Za-z]{3,9}\. \d{1,2}$', date_str):
        return f"{date_str}, {year}"
    return date_str

def fetch_spreadsheet_data():
    """Fetch data from the spreadsheet and inspect it"""
    # Determine which sheet to use
    sheet_names = get_sheet_names()
    if not sheet_names:
        print("Could not retrieve sheet names.")
        return
    
    if not SHEET_NAME:
        sheet_to_use = sheet_names[0]
        print(f"No SHEET_NAME specified in .env, using first sheet: {sheet_to_use}")
    else:
        if SHEET_NAME not in sheet_names:
            print(f"Warning: Specified SHEET_NAME '{SHEET_NAME}' not found in spreadsheet.")
            print(f"Available sheets: {', '.join(sheet_names)}")
            sheet_to_use = sheet_names[0]
            print(f"Using first sheet instead: {sheet_to_use}")
        else:
            sheet_to_use = SHEET_NAME
    
    # Fetch the data
    range_name = f"{sheet_to_use}!A1:G100"
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_name}?key={API_KEY}"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: API request failed with status {response.status_code}")
            print(response.text)
            return
        
        result = response.json()
        values = result.get('values', [])
        
        if not values:
            print("No data found in spreadsheet")
            return
        
        headers = values[0]
        data = values[1:]
        
        print(f"\n===== SPREADSHEET DATA =====")
        print(f"Headers: {headers}")
        print(f"Number of data rows: {len(data)}")
        
        # Look for date column
        date_col_idx = -1
        for i, header in enumerate(headers):
            if header.lower() == 'date':
                date_col_idx = i
                break
        
        if date_col_idx == -1:
            print("\nNo 'date' column found!")
            return
        
        print(f"\n===== DATE VALUES =====")
        for i, row in enumerate(data[:10]):  # Show first 10 rows
            if len(row) > date_col_idx:
                date_val = row[date_col_idx]
                print(f"Row {i+1}: '{date_val}'")
                
                # Try to detect format
                if re.match(r'\d{4}-\d{2}-\d{2}', date_val):
                    print(f"  ↳ Appears to be ISO format (YYYY-MM-DD)")
                elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_val):
                    print(f"  ↳ Appears to be MM/DD/YYYY or DD/MM/YYYY")
                elif re.match(r'\d{1,2}\.\d{1,2}\.\d{4}', date_val):
                    print(f"  ↳ Appears to be DD.MM.YYYY or MM.DD.YYYY")
                elif re.match(r'[A-Za-z]{3,9} \d{1,2}, \d{4}', date_val):
                    print(f"  ↳ Appears to be Month DD, YYYY")
                elif re.match(r'[A-Za-z]{3,9}\. \d{1,2}$', date_val):
                    print(f"  ↳ WARNING: Appears to be Month. DD missing year - This will cause errors!")
                    
                    # Show how it would look with year
                    fixed_date = add_year_to_dates(date_val)
                    print(f"     Fixed version: '{fixed_date}'")
                    
                    # Try parsing
                    try:
                        parsed_date = pd.to_datetime(fixed_date)
                        print(f"     Would parse as: {parsed_date.strftime('%Y-%m-%d')}")
                    except:
                        print(f"     Still can't parse with added year")
            else:
                print(f"Row {i+1}: Missing date value")
        
        # Test automatic fixing
        has_abbreviated_dates = any(re.match(r'[A-Za-z]{3,9}\. \d{1,2}$', row[date_col_idx]) 
                                   for row in data if len(row) > date_col_idx)
        
        if has_abbreviated_dates:
            print("\n===== AUTOMATIC FIX TEST =====")
            print("Testing automatic date fixing with current year...")
            
            current_year = datetime.now().year
            fixed_dates = [add_year_to_dates(row[date_col_idx], current_year) 
                          if len(row) > date_col_idx else "" for row in data]
            
            # Try parsing all fixed dates
            try:
                parsed_dates = pd.to_datetime(fixed_dates, errors='coerce')
                valid_count = parsed_dates.notna().sum()
                print(f"Successfully parsed {valid_count} out of {len(fixed_dates)} dates after adding year {current_year}")
                
                if valid_count == len(fixed_dates):
                    print("✅ All dates successfully fixed!")
                else:
                    print(f"❌ {len(fixed_dates) - valid_count} dates still have issues")
            except Exception as e:
                print(f"Error during parsing: {str(e)}")
        
        print("\n===== RECOMMENDED SOLUTION =====")
        if has_abbreviated_dates:
            print("Your spreadsheet uses abbreviated dates without years (e.g. 'Jan. 11').")
            print("The code has been updated to handle this automatically by adding the current year.")
            print("No changes to your spreadsheet are needed.")
        else:
            print("Based on the date values, you should update your spreadsheet to:")
            print("1. Ensure all date cells contain complete dates with year")
            print("2. Use a consistent date format (preferably YYYY-MM-DD)")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Inspecting spreadsheet data...\n")
    fetch_spreadsheet_data()
