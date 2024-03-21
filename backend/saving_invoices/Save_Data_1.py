import os
import shutil
import mysql.connector



 
# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vim"
)
cursor = db.cursor()



 
# Function to move files and log entry in database
def move_files_and_log(folder_path, destination_folder):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            # Get subfolder name
            subfolder_name = os.path.basename(root)

            #print(subfolder_name)
            # Generate unique ID
            unique_id = f"{subfolder_name}_{file}"

            # New file name with the unique ID
            new_file_name = f"{unique_id}"

            # New file path with the unique ID
            new_file_path = os.path.join(destination_folder, new_file_name)

            # Check if file exists in database
            cursor.execute("SELECT * FROM Invoice_Master WHERE UniqueId = %s", (unique_id,))
            existing_entry = cursor.fetchone()
            if existing_entry:
                # Update file location in database
                cursor.execute("UPDATE Invoice_Master SET DestinationFolder = %s WHERE UniqueId = %s", (destination_folder, unique_id))
                db.commit()
                # Move file to new location
                try:
                    shutil.move(file_path, new_file_path)
                    status = "Success"
                except Exception as e:
                    status = "Failed"
                    print(f"Failed to move file: {e}")
                finally:
                    print(f"File: {file}, Status: {status}")
            else:
                # Log entry in database for new file
                try:
                    
                    cursor.execute("INSERT INTO invoice_master (UniqueId, MailId, FileName, DestinationFolder, Status) VALUES (%s, %s, %s, %s, %s)",
                                   (unique_id, subfolder_name, file, destination_folder, "Pending"))
                    db.commit()
                    print(f"File: {file}, Status: Success")
                    shutil.move(file_path, new_file_path)
                except Exception as e:
                    print(f"Failed to move file: {e}")
 

# Example usage
folder_path = r'D:\BSC\BSC_2024\VIM\backend\email_stubbing\mail_pdf_data'
destination_folder = r'D:\BSC\BSC_2024\VIM\backend\saving_invoices\invoice_documents'
move_files_and_log(folder_path, destination_folder)

# Close database connection
db.close()