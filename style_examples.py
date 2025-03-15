"""
Example of how to use styling in Great Tables
Run this script to see examples of different styling options
"""

import pandas as pd
from great_tables import GT
from datetime import datetime

def show_gt_styling_examples():
    """Show examples of different styling options in Great Tables"""
    # Create sample data
    data = {
        'week': ['1', '2', '3'],
        'date': [datetime(2024, 1, 11), datetime(2024, 1, 18), datetime(2024, 1, 25)],
        'topic': ['Introduction', 'Data Analysis', 'Visualization'],
        'notes': ['Important', 'Take quiz', 'Bring laptop']
    }
    
    df = pd.DataFrame(data)
    
    print("===== GREAT TABLES STYLING EXAMPLES =====")
    
    # Basic table
    print("\nBasic example with borders:")
    
    gt = GT(df)
    
    # Add borders to specific columns
    styled_gt = (
        gt
        .fmt_date(columns="date", date_style="day_m")
        # Add right border to date column headers
        .tab_style(
            style={"border-right": "1px solid #D3D3D3"},
            locations="cells:column_labels(date)"
        )
        # Add right border to date column cells
        .tab_style(
            style={"border-right": "1px solid #D3D3D3"},
            locations="cells:body(columns('date'))"
        )
        # Print the table representation
        .as_raw_html()
    )
    
    print(f"Generated table HTML (first 100 chars): {styled_gt[:100]}...")
    
    print("\nLocation specifiers in Great Tables (Python):")
    print("- cells:body()")
    print("- cells:column_labels()")
    print("- cells:row_groups()")
    print("- cells:column_spanners()")
    print("- cells:stub()")
    print("- cells:stub_head()")
    
    print("\nFor specific columns:")
    print("- cells:body(columns(col_name))")
    print("- cells:column_labels(col_name)")
    
    print("\nFor specific rows:")
    print("- cells:body(rows(row_indices))")
    
    print("\n===== CORRECT USAGE FOR YOUR CODE =====")
    print("For each column that needs a right border:")
    print("""
    .tab_style(
        style={"border-right": "1px solid #D3D3D3"},
        locations="cells:column_labels(column_name)"
    )
    .tab_style(
        style={"border-right": "1px solid #D3D3D3"},
        locations="cells:body(columns('column_name'))"
    )
    """)

if __name__ == "__main__":
    show_gt_styling_examples()
