import imaplib
import email
import os
 
# Email credentials
email_user = 'vijaybsingh1999@gmail.com'
email_password = 'uelfhrwgphxqnhwh'
imap_url = 'imap.gmail.com'
folder_path = r'D:\BSC\BSC_2024\VIM\backend\email_stubbing\mail_pdf_data' # Specify the path where you want the folders to be created
 
# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_url)
mail.login(email_user, email_password)
 
# Select the inbox folder
mail.select('inbox')
 
# Search for all unseen emails
status, data = mail.search(None, '(UNSEEN)')
 
for num in data[0].split():
    # Fetch the email
    status, data = mail.fetch(num, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
 
    # Get the sender's email address
    sender_email = email.utils.parseaddr(email_message['From'])[1]
 
    # Create a folder with the sender's email ID
    sender_folder_path = os.path.join(folder_path, sender_email)
    if not os.path.exists(sender_folder_path):
        os.makedirs(sender_folder_path)
 
    # Iterate through the email attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
 
        # Download the attachment
        filename = part.get_filename()
        filepath = os.path.join(sender_folder_path, filename)
 
        # Check if the file already exists
        if os.path.exists(filepath):
            # Update the file if it already exists
            os.remove(filepath)
 
        # Save the attachment
        with open(filepath, 'wb') as f:
            f.write(part.get_payload(decode=True))
 
# Close the connection
mail.close()
mail.logout()