import os
import pandas as pd
import mysql.connector
from datetime import datetime

# Connect to MySQL database
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="vim"
    )

# Function to fetch 'Pending' records from MySQL and update 'Pending' records to 'Success'
def update_status_and_export_to_csv(connection, destination_folder):
    cursor = connection.cursor()

    # Fetch 'Pending' records
    cursor.execute("SELECT * FROM Invoice_Details WHERE Status = 'Pending'")
    pending_records = cursor.fetchall()

    if not pending_records:
        print("No pending records found.")
        return

    # Create DataFrame with pending records
    df = pd.DataFrame(pending_records, columns=[i[0] for i in cursor.description])

    # Replace null values with "NULL"
    df.fillna("NULL", inplace=True)

    # Check if CSV file already exists
    csv_filename = os.path.join(destination_folder, 'table_data.csv')
    if os.path.exists(csv_filename):
        # Load existing CSV file and concatenate new data
        existing_df = pd.read_csv(csv_filename)
        df = pd.concat([existing_df, df], ignore_index=True)

    # Write DataFrame to CSV with "NULL" representation for NaN values
    df.to_csv(csv_filename, index=False, na_rep="NULL")


    # Update status to 'Success' for 'Pending' records
    cursor.execute("UPDATE Invoice_Details SET Status = 'Success' WHERE Status = 'Pending'")
    connection.commit()
    print("Records updated successfully. CSV file stored at:", csv_filename)

# Main function
def main():
    connection = connect_to_mysql()
    if connection.is_connected():
        print("Connected to MySQL database.")
        destination_folder = r'D:\BSC\BSC_2024\VIM\backend\csv_master\CSV_Files'  # Specify your destination folder here

        update_status_and_export_to_csv(connection, destination_folder)

        connection.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
