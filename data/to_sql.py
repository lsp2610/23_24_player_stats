import pandas as pd
import sqlite3

# Step 1: Define the Excel file and list of sheet names
excel_file = r'data\23_24 Player Stats Data - FBRef.xlsx'  # Path to your Excel file
sheet_names = ['shooting', 'passing', 'pass_types', 'gca', 'defensive_actions',
               'possession', 'playing_time', 'misc']  # List of sheet names to import

# Step 2: Create a connection to the SQLite database
conn = sqlite3.connect(r'C:\Users\Owner\dev\23_24_player_stats\data\23_24_player_stats.db')  # Path to your SQLite database

# Step 3: Loop through the sheet names
for sheet_name in sheet_names:
    # Read each sheet into a DataFrame
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    # Filter out non-numeric columns to perform aggregations
    numeric_columns = df.select_dtypes(include='number').columns.tolist()
    non_agg_columns = ['Age', 'Born', '90s', 'Rk', 'Nation', 'Pos', 'Squad', 'Comp', 'Matches']  # Columns that shouldn't be averaged
    numeric_columns_to_avg = [col for col in numeric_columns if col not in non_agg_columns]
    
    # Perform the aggregation
    agg_funcs = {col: 'mean' for col in numeric_columns_to_avg}
    agg_funcs['90s'] = 'sum'
    df_agg = df.groupby('Player').agg(agg_funcs).reset_index()
    
    # Select non-numeric columns to merge back
    non_numeric_columns = ['Player', 'Age', 'Born', 'Nation', 'Pos', 'Squad', 'Comp', 'Matches']
    df_non_numeric = df[non_numeric_columns].drop_duplicates(subset='Player')
    
    # Merge back the non-aggregated columns
    df_final = df_non_numeric.merge(df_agg, on='Player', how='right')
    
    # Define the table name (you can customize this as needed)
    table_name = sheet_name
    
    # Write the aggregated DataFrame to the SQLite database
    df_final.to_sql(table_name, conn, if_exists='replace', index=False)

    # Verify the data in SQLite (optional)
    df_from_db = pd.read_sql(f'SELECT * FROM {table_name}', conn)
    print(f"Data from {table_name}:")
    print(df_from_db.head())

# Step 4: Close the connection
conn.close()