from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
from flask import Flask, jsonify, send_file, abort
import os

app = Flask(__name__)  # Change '__InvoiceNumber__' to '__name__'
CORS(app)

# MySQL Configuration
db = pymysql.connect(host='localhost',
                     user='root',
                     password='',
                     database='vim',
                     cursorclass=pymysql.cursors.DictCursor)

@app.route('/api/data', methods=['GET'])
def get_data():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Invoice_Master")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def add_data():
    data = request.json
    cursor = db.cursor()
    cursor.execute("INSERT INTO Invoices (InvoiceNumber, InvoiceDate, DeliveryNote, VendorName, PONumber, VAT_GST_ID, TotalAmount, CompanyName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                   (data['InvoiceNumber'], data['InvoiceDate'], data['DeliveryNote'], data['VendorName'], data['PONumber'], data['VAT_GST_ID'], data['TotalAmount'], data['CompanyName']))
    db.commit()
    return 'Data added successfully'

@app.route('/api/data/<int:InvoiceNumber>', methods=['PUT'])
def update_data(InvoiceNumber):
    data = request.json
    cursor = db.cursor()
    cursor.execute("UPDATE Invoices SET InvoiceNumber=%s, InvoiceDate=%s, DeliveryNote=%s, VendorName=%s, PONumber=%s, VAT_GST_ID=%s, TotalAmount=%s, CompanyName=%s WHERE InvoiceNumber=%s",
                   (data['InvoiceNumber'], data['InvoiceDate'], data['DeliveryNote'], data['VendorName'], data['PONumber'], data['VAT_GST_ID'], data['TotalAmount'], data['CompanyName'], InvoiceNumber))
    db.commit()
    return 'Data updated successfully'

@app.route('/api/data/<int:InvoiceNumber>', methods=['DELETE'])
def delete_data(InvoiceNumber):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Invoices WHERE InvoiceNumber=%s", (InvoiceNumber,))
    db.commit()
    return 'Data deleted successfully', 200

@app.route('/api/data/filter', methods=['GET'])
def filter_data():
    company_name = request.args.get('companyName')
    cursor = db.cursor()
    query = "SELECT * FROM Invoices WHERE CompanyName = %s"
    cursor.execute(query, (company_name,))
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        # Respond to preflight request
        headers = {
            'Access-Control-Allow-Origin': '*',  # Adjust as needed
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'  # Cache preflight response for 1 hour
        }
        return ('', 204, headers)
    
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Query the database to check if the user exists and the password matches
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401
    

@app.route('/api/invoices/<path:filepath>/preview')
def preview_invoice(filepath):
    try:
        # Construct the full file path
        full_file_path = os.path.join('destination_folder', filepath)
       
        # Check if the file exists
        if os.path.exists(full_file_path):
            # Serve the file
            return send_file(full_file_path, as_attachment=False)
        else:
            # Return a 404 error if the file is not found
            abort(404)
    except Exception as e:
        # Return a 500 error if any unexpected error occurs
        print("Error previewing invoice:", e)
        abort(500)


if __name__ == '__main__':
    app.run(debug=True)
    destination_folder = r'D:\BSC\BSC_2024\VIM\backend\saving_invoices\invoice_documents'
