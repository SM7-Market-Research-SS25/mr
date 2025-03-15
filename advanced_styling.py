"""
Advanced styling exploration for Great Tables
"""

import pandas as pd
from great_tables import GT, Loc, cells_body, cells_column_labels
from datetime import datetime

def explore_styling_options():
    """Explore different ways to apply styling in Great Tables"""
    # Sample data
    data = {
        'week': ['1', '2', '3'],
        'date': [datetime(2024, 1, 11), datetime(2024, 1, 18), datetime(2024, 1, 25)],
        'topic': ['Introduction', 'Data Analysis', 'Visualization'],
        'notes': ['Important', 'Take quiz', 'Bring laptop']
    }
    
    df = pd.DataFrame(data)
    
    print("Testing different styling approaches in Great Tables...")
    
    # Approach 1: Using Loc objects directly
    try:
        print("\nApproach 1: Using Loc objects")
        gt1 = GT(df)
        styled_gt1 = (
            gt1
            .tab_style(
                style={"border-right": "1px solid #D3D3D3"},
                locations=Loc(cells_body(), cells_column_labels(), columns="date")
            )
            .as_raw_html()
        )
        print("✅ Success")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Approach 2: Using cells functions
    try:
        print("\nApproach 2: Using cells functions")
        gt2 = GT(df)
        styled_gt2 = (
            gt2
            .tab_style(
                style={"border-right": "1px solid #D3D3D3"},
                locations=[cells_body(columns="date"), cells_column_labels(columns="date")]
            )
            .as_raw_html()
        )
        print("✅ Success")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # Approach 3: Simple styling without borders
    try:
        print("\nApproach 3: Simple styling without borders")
        gt3 = GT(df)
        styled_gt3 = (
            gt3
            .fmt_date(columns="date", date_style="day_m")
            .cols_align(align="center", columns=["week"])
            .cols_align(align="right", columns=["date"])
            .cols_align(align="left", columns=["topic", "notes"])
            .as_raw_html()
        )
        print("✅ Success")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print("\nRecommendation for your index.qmd:")
    print("1. Start with the simple styling approach (no borders)")
    print("2. If borders are critical, try importing the Loc class and cells functions")
    print("   from great_tables and use approach 2")
    
    # Show example code to add to index.qmd
    print("\nSample code to add borders (if needed):")
    print("""
# At the top of your file:
from great_tables import GT, cells_body, cells_column_labels

# In your table styling:
gt_table
.tab_style(
    style={"border-right": "1px solid #D3D3D3"},
    locations=[cells_body(columns="date"), cells_column_labels(columns="date")]
)
.tab_style(
    style={"border-right": "1px solid #D3D3D3"},
    locations=[cells_body(columns="topic"), cells_column_labels(columns="topic")]
)
# ...and so on for other columns
    """)

if __name__ == "__main__":
    explore_styling_options()
