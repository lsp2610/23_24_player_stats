import pandas as pd
import sqlite3

# Step 1: Define the Excel file and list of sheet names
excel_file = r'data\23_24 Player Stats Data - FBRef.xlsx'  # Path to your Excel file
sheet_names = ['shooting', 'passing', 'pass_types', 'gca', 'defensive_actions',
               'possession', 'playing_time', 'misc']  # List of sheet names to import

# Step 2: Create a connection to the SQLite database
conn = sqlite3.connect('23_24_player_stats.db')  # Path to your SQLite database

# Step 3: Loop through the sheet names
for sheet_name in sheet_names:
    # Read each sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Define the table name (you can customize this as needed)
    table_name = sheet_name
    
    # Write the DataFrame to the SQLite database
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Verify the data in SQLite (optional)
    df_from_db = pd.read_sql(f'SELECT * FROM {table_name}', conn)
    print(f"Data from {table_name}:")
    print(df_from_db.head())

# Step 4: Close the connection
conn.close()
