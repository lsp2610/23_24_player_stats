import pandas as pd
import sqlite3

# Define the CSV file path and the SQLite database path
csv_file_path = r'C:\Users\Owner\dev\23_24_player_stats\data\team_stats.csv'  # Path to your CSV file
sqlite_db_path = r'C:\Users\Owner\dev\23_24_player_stats\data\23_24_player_stats.db'  # Path to your SQLite database

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(sqlite_db_path)

# Define the table name (you can customize this as needed)
table_name = 'your_table_name'

# Write the DataFrame to the SQLite database
df.to_sql(table_name, conn, if_exists='replace', index=False)

# Verify the data in SQLite (optional)
df_from_db = pd.read_sql(f'SELECT * FROM {table_name}', conn)
print(f"Data from {table_name}:")
print(df_from_db.head())

# Close the connection
conn.close()