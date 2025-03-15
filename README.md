# Market Research Course Materials

## Setting Up Google Sheets API

This project uses data from a Google Spreadsheet. To make it work:

### 1. Make your Google Sheet publicly accessible

1. Open your spreadsheet in Google Sheets: [https://docs.google.com/spreadsheets/d/1R7WY6LYa9EkiArXnRm-jRAXa_MYx6GmZX5g55vHqxBU](https://docs.google.com/spreadsheets/d/1R7WY6LYa9EkiArXnRm-jRAXa_MYx6GmZX5g55vHqxBU)
2. Click the "Share" button in the top right
3. In the window that appears:
   - Click "Change to anyone with the link"
   - Make sure "Viewer" is selected
   - Click "Done"

### 2. Create your environment file

Create a `.env` file in your project directory with the following content:

```
GOOGLE_SHEETS_API_KEY=AIzaSyBJ2wbHblOe8G6w-V5tEcfzlAFldz1qmoU
SPREADSHEET_ID=1R7WY6LYa9EkiArXnRm-jRAXa_MYx6GmZX5g55vHqxBU
SHEET_NAME=YourSheetNameHere
```

Note: The `SHEET_NAME` should match exactly the name of your worksheet tab in Google Sheets (not "Sheet1" unless that's actually the name).

### 3. Test your connection

Run the test script to make sure everything is working:

```bash
python test_api.py
```

This will also tell you the correct sheet name to use in your .env file.

### Expected Spreadsheet Format

Your spreadsheet should have the following columns:
- week 
- date
- topic
- prepare
- materials
- due

The first row should contain the headers.

# Setup

## uv

uv init . --python 3.11  

uv sync

source .venv/bin/activate

uv add python-dotenv pandas requests great_tables jupyter pyyaml

touch .env

## quarto

quarto publish gh-pages --no-browser