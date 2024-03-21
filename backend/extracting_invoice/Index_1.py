from azure.core.exceptions import HttpResponseError
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

import mysql.connector
#import sqlite3


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vim"
)
cursor = db.cursor()




# Connect to your database
#conn = sqlite3.connect('vim.db')
#cursor = conn.cursor()

# Execute the query to fetch rows with 'Status' as 'Pending'
cursor.execute("SELECT * FROM Invoice_Master WHERE status = 'Pending'")
rows = cursor.fetchall()

# Create a list to hold dictionaries for each row
Invoice_Data_Pending_Records_List = []

# Iterate through the rows and create dictionaries
for row in rows:
    Invoice_Details_From_Database_Dict = {}
    for idx, column in enumerate(cursor.description):
        Invoice_Details_From_Database_Dict[column[0]] = row[idx]
    Invoice_Data_Pending_Records_List.append(Invoice_Details_From_Database_Dict)
    Invoice_Details_From_Database_Dict = {}

# Fetch the values by field name
for index, record in enumerate(Invoice_Data_Pending_Records_List):
    # Accessing dictionary values by field name
    Unique_Id = record['UniqueId']
    Mail_Id = record['MailId']
    File_Name = record['FileName']
    Destination_Folder = record['DestinationFolder']
    # Similarly, access other fields as needed
    #print(f"Invoice ID: {invoice_id}, Invoice Number: {invoice_number}")
    # Print other fields as needed


    try:
        endpoint = "https://avdhut.cognitiveservices.azure.com/"
        key = "237f2f1269964732844dc0f0a24e12d0"
        formUrl = "https://iservevendor.com/Indodev/functionFiles/upload_download/"+File_Name
    
        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
    
        poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-invoice", formUrl)
    
        while not poller.done():
            print("Polling...")
            poller.wait(15)
    
        invoices = poller.result()
    
        # Defining Dictionary for saving extacted vendor data
        invoice_Extracted_Vendor_Data = {}
    
        for idx, invoice in enumerate(invoices.documents):
            print("*******************************************************")
            print("--------Recognizing invoice #{}--------".format(index + 1))
            print("*******************************************************")
    
        
            vendor_name = invoice.fields.get("VendorName")
            if vendor_name:
                invoice_Extracted_Vendor_Data["VendorName"] = vendor_name.value
            else:
                invoice_Extracted_Vendor_Data["VendorName"] = None
    
    
            vendor_address = invoice.fields.get("VendorAddress")
            if vendor_address:
                invoice_Extracted_Vendor_Data["VendorAddress"] = vendor_address.content
            else:
                invoice_Extracted_Vendor_Data["VendorAddress"] = None
            
        
            vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
            if vendor_address_recipient:
                invoice_Extracted_Vendor_Data["VendorAddressRecipient"] =   vendor_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["VendorAddressRecipient"] = None
            
    
            customer_name = invoice.fields.get("CustomerName")
            if customer_name:
                invoice_Extracted_Vendor_Data["CustomerName"] = customer_name.value
            else:
                invoice_Extracted_Vendor_Data["CustomerName"] = None
            

            customer_id = invoice.fields.get("CustomerId")
            if customer_id:
                invoice_Extracted_Vendor_Data["CustomerId"] = customer_id.value
            else:
                invoice_Extracted_Vendor_Data["CustomerId"] = None
            

            customer_address = invoice.fields.get("CustomerAddress")
            if customer_address:
                invoice_Extracted_Vendor_Data["CustomerAddress"] = customer_address.content
            else:
                invoice_Extracted_Vendor_Data["CustomerAddress"] = None
            
    
            customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
            if customer_address_recipient:
                invoice_Extracted_Vendor_Data["CustomerAddressRecipient"] = customer_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["CustomerAddressRecipient"] = None
            
    
            invoice_id = invoice.fields.get("InvoiceId")
            if invoice_id:
                invoice_Extracted_Vendor_Data["InvoiceId"] = invoice_id.value
            else:
                invoice_Extracted_Vendor_Data["InvoiceId"] = None
            

            invoice_date = invoice.fields.get("InvoiceDate")
            if invoice_date:
                formatted_date = invoice_date.value.strftime("%Y-%m-%d")
                invoice_Extracted_Vendor_Data["InvoiceDate"] = formatted_date
            else:
                invoice_Extracted_Vendor_Data["InvoiceDate"] = None
            

            invoice_total = invoice.fields.get("InvoiceTotal")
            if invoice_total:
                invoice_Extracted_Vendor_Data["InvoiceTotal"] = "{:.2f}".format(float(invoice_total.value.amount))
            else:
                invoice_Extracted_Vendor_Data["InvoiceTotal"] = None
            
    
            due_date = invoice.fields.get("DueDate")
            if due_date:
                invoice_Extracted_Vendor_Data["DueDate"] = due_date.value
            else:
                invoice_Extracted_Vendor_Data["DueDate"] = None
            

            purchase_order = invoice.fields.get("PurchaseOrder")
            if purchase_order: 
                invoice_Extracted_Vendor_Data["PurchaseOrder"] = purchase_order.value
            else:
                invoice_Extracted_Vendor_Data["PurchaseOrder"] = None
            

            billing_address = invoice.fields.get("BillingAddress")
            if billing_address:
                invoice_Extracted_Vendor_Data["BillingAddress"] = billing_address.content
            else:
                invoice_Extracted_Vendor_Data["BillingAddress"] = None
            

            billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
            if billing_address_recipient: 
                invoice_Extracted_Vendor_Data["BillingAddressRecipient"] = billing_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["BillingAddressRecipient"] = None
            

            shipping_address = invoice.fields.get("ShippingAddress")
            if shipping_address:
                if hasattr(shipping_address, 'replace'):  # Check if the object has a replace method
                    invoice_Extracted_Vendor_Data["ShippingAddress"] = shipping_address.value
                else:
                    invoice_Extracted_Vendor_Data["ShippingAddress"] = str(shipping_address.value)  # Convert to string if necessary
            else:
                invoice_Extracted_Vendor_Data["ShippingAddress"] = None
            

            shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
            if shipping_address_recipient:
                invoice_Extracted_Vendor_Data["ShippingAddressRecipient"] = shipping_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["ShippingAddressRecipient"] = None
            

            subtotal = invoice.fields.get("SubTotal")
            if subtotal:
                invoice_Extracted_Vendor_Data["SubTotal"] = "{:.2f}".format(float( subtotal.value.amount))
            else:
                invoice_Extracted_Vendor_Data["SubTotal"] = None
            

            total_tax = invoice.fields.get("TotalTax")
            if total_tax:
                invoice_Extracted_Vendor_Data["TotalTax"] = "{:.2f}".format(float( total_tax.value.amount))
            else:
                invoice_Extracted_Vendor_Data["TotalTax"] = None
            
    
    
            previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
            if previous_unpaid_balance:
                invoice_Extracted_Vendor_Data["PreviousUnpaidBalance"] = "{:.2f}".format(float( previous_unpaid_balance.value.amount))
            else:
                invoice_Extracted_Vendor_Data["PreviousUnpaidBalance"] = None
            

    
            amount_due = invoice.fields.get("AmountDue")
            if amount_due:
                invoice_Extracted_Vendor_Data["AmountDue"] = "{:.2f}".format(float( amount_due.value.amount))
            else:
                invoice_Extracted_Vendor_Data["AmountDue"] = None
            

    
            service_start_date = invoice.fields.get("ServiceStartDate")
            if service_start_date:
                invoice_Extracted_Vendor_Data["ServiceStartDate"] = service_start_date.value
            else:
                invoice_Extracted_Vendor_Data["ServiceStartDate"] = None
            
    
    
            service_end_date = invoice.fields.get("ServiceEndDate")
            if service_end_date:
                invoice_Extracted_Vendor_Data["ServiceEndDate"] = service_end_date.value
            else:
                invoice_Extracted_Vendor_Data["ServiceEndDate"] = None
            
    
    
            service_address = invoice.fields.get("ServiceAddress")
            if service_address:
                invoice_Extracted_Vendor_Data["ServiceAddress"] = service_address.value
            else:
                invoice_Extracted_Vendor_Data["ServiceAddress"] = None
            

    
            service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
            if service_address_recipient:
                invoice_Extracted_Vendor_Data["ServiceAddressRecipient"] =  service_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["ServiceAddressRecipient"] = None
            


    
            remittance_address = invoice.fields.get("RemittanceAddress")
            if remittance_address:
                invoice_Extracted_Vendor_Data["RemittanceAddress"] = remittance_address.value
            else:
                invoice_Extracted_Vendor_Data["RemittanceAddress"] = None
            


    
            remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
            if remittance_address_recipient:
                invoice_Extracted_Vendor_Data["RemittanceAddressRecipient"] = remittance_address_recipient.value
            else:
                invoice_Extracted_Vendor_Data["RemittanceAddressRecipient"] = None
            



        #Creating List for saving extracted Line Items
            
        invoice_Extracted_Material_Data = []   

        #Creating dictionary for multiple line item
        
        invoice_Extracted_Line_Item_Data= {}

        print("Invoice items:")
        for idx, item in enumerate(invoice.fields.get("Items").value):
        
        # print("...Item #{}".format(idx + 1))
        
        
            item_description = item.value.get("Description")
            if item_description:
                invoice_Extracted_Line_Item_Data["Description"] = item_description.value
            else:
                invoice_Extracted_Vendor_Data["Description"] = None
            
    
    
            item_quantity = item.value.get("Quantity")
            if item_quantity:
                invoice_Extracted_Line_Item_Data["Quantity"] =item_quantity.value
            else:
                invoice_Extracted_Vendor_Data["Quantity"] = None
            
    
            unit = item.value.get("Unit")
            if unit:
                invoice_Extracted_Line_Item_Data["Unit"] = unit.value
            else:
                invoice_Extracted_Vendor_Data["Unit"] = None
            

    
    
            unit_price = item.value.get("UnitPrice")
            if unit_price:
                invoice_Extracted_Line_Item_Data["UnitPrice"] = "{:.2f}".format(float( unit_price.value.amount))
            else:
                invoice_Extracted_Vendor_Data["UnitPrice"] = None
            


    
            product_code = item.value.get("ProductCode")
            if product_code:
                invoice_Extracted_Line_Item_Data["ProductCode"] = product_code.value
            else:
                invoice_Extracted_Vendor_Data["ProductCode"] = None
            


    
            item_date = item.value.get("Date")
            if item_date:
                invoice_Extracted_Line_Item_Data["Date"] = item_date.value
            else:
                invoice_Extracted_Vendor_Data["Date"] = None
            


    
            tax = item.value.get("Tax")
            if tax:
                invoice_Extracted_Line_Item_Data["Tax"] = "{:.2f}".format(float(tax.value.amount))
            else:
                invoice_Extracted_Vendor_Data["Tax"] = None
            


    
            amount = item.value.get("Amount")
            if amount:
                invoice_Extracted_Line_Item_Data["Amount"] = "{:.2f}".format(float(amount.value.amount))
            else:
                invoice_Extracted_Vendor_Data["Amount"] = None
            



            

        
            invoice_Extracted_Material_Data.append(invoice_Extracted_Line_Item_Data)
            invoice_Extracted_Line_Item_Data = {}


        #print(invoice_Extracted_Material_Data)
        print(invoice_Extracted_Vendor_Data)

        # Iterate over each element with its index
        for index, value in enumerate(invoice_Extracted_Material_Data):
        
            cursor.execute("INSERT INTO Invoice_Details (UniqueId, MailId, FileName, DestinationFolder, Status, LineItemNumber, VendorName, VendorAddress, VendorAddressRecipient, CustomerName, CustomerId, CustomerAddress, CustomerAddressRecipient,InvoiceId, InvoiceDate, InvoiceTotal, DueDate, PurchaseOrder,BillingAddress, BillingAddressRecipient, ShippingAddress, ShippingAddressRecipient,SubTotal, TotalTax, PreviousUnpaidBalance, AmountDue, ServiceStartDate, ServiceEndDate, ServiceAddress, ServiceAddressRecipient,RemittanceAddress, RemittanceAddressRecipient,Description, Quantity, Unit, UnitPrice, ProductCode,Date, Tax, Amount) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (Unique_Id, Mail_Id, File_Name, Destination_Folder, "Pending", index+1, invoice_Extracted_Vendor_Data['VendorName'], invoice_Extracted_Vendor_Data['VendorAddress'], invoice_Extracted_Vendor_Data['VendorAddressRecipient'], invoice_Extracted_Vendor_Data['CustomerName'], invoice_Extracted_Vendor_Data['CustomerId'], invoice_Extracted_Vendor_Data['CustomerAddress'], invoice_Extracted_Vendor_Data['CustomerAddressRecipient'], invoice_Extracted_Vendor_Data['InvoiceId'], invoice_Extracted_Vendor_Data['InvoiceDate'], invoice_Extracted_Vendor_Data['InvoiceTotal'], invoice_Extracted_Vendor_Data['DueDate'], invoice_Extracted_Vendor_Data['PurchaseOrder'], invoice_Extracted_Vendor_Data['BillingAddress'], invoice_Extracted_Vendor_Data['BillingAddressRecipient'],
                        invoice_Extracted_Vendor_Data['ShippingAddress'], invoice_Extracted_Vendor_Data['ShippingAddressRecipient'], invoice_Extracted_Vendor_Data['SubTotal'], invoice_Extracted_Vendor_Data['TotalTax'], invoice_Extracted_Vendor_Data['PreviousUnpaidBalance'], invoice_Extracted_Vendor_Data['AmountDue'], invoice_Extracted_Vendor_Data['ServiceStartDate'], invoice_Extracted_Vendor_Data['ServiceEndDate'], invoice_Extracted_Vendor_Data['ServiceAddress'], invoice_Extracted_Vendor_Data['ServiceAddressRecipient'], invoice_Extracted_Vendor_Data['RemittanceAddress'], invoice_Extracted_Vendor_Data['RemittanceAddressRecipient'],
                            value.get("Description",None), value.get("Quantity",None), value.get("Unit",None), value.get("UnitPrice",None), value.get("ProductCode",None), value.get("Date",None), value.get("Tax",None), value.get("Amount",None)  )) 
        
        #db.commit()
        
        #  print(f"Index: {index}, Value: {value}")
            
        print("Invoice Fields Inserted successfully")
        

        cursor.execute("UPDATE Invoice_Master SET Status = 'Success' WHERE UniqueId = %s",(Unique_Id,))

        db.commit()


 
 
    except HttpResponseError as e:
        print("Form recognizer service returned error:")
        print(e.message)
        print(f"Error code: {e.error.code}")
 
        # You can also print the status
        print(f"Status code: {e.response.status_code}")
 
     # Success
    else:
        print("Invoice analysis completed successfully. status = 200")
        print(invoice_Extracted_Vendor_Data)
        print("************************************")
        print("Final List----------")
    print(invoice_Extracted_Material_Data)








# Close the connection
db.close()











"""Unique_Id = cursor.execute("SELECT UniqueId FROM Invoice_Master WHERE Status='Pending' ")
Mail_Id = cursor.execute("SELECT MailId FROM Invoice_Master WHERE Status='Pending' ")
File_Name = cursor.execute("SELECT FileName FROM Invoice_Master WHERE Status='Pending' ")
Destination_Folder = cursor.execute("SELECT DestinationFolder FROM Invoice_Master WHERE Status='Pending' ")

Invoice_Details_From_Database_Dict = {}
 
Invoice_Details_From_Database_Dict['UniqueId'] = Unique_Id
Invoice_Details_From_Database_Dict['MailId'] = Mail_Id
Invoice_Details_From_Database_Dict['FileName'] = File_Name
Invoice_Details_From_Database_Dict['DestinationFolder'] = Destination_Folder

Invoice_Data_List = []

Invoice_Data_List.append(Invoice_Details_From_Database_Dict)   """









 
"""try:
    endpoint = "https://avdhut.cognitiveservices.azure.com/"
    key = "237f2f1269964732844dc0f0a24e12d0"
    formUrl = "https://iservevendor.com/Indodev/functionFiles/upload_download/"+File_Name
 
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
   
    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-invoice", formUrl)
 
    while not poller.done():
        print("Polling...")
        poller.wait(15)
 
    invoices = poller.result()
 
    # Defining Dictionary for saving extacted vendor data
    invoice_Extracted_Vendor_Data = {}
 
    for idx, invoice in enumerate(invoices.documents):
        print("--------Recognizing invoice #{}--------".format(idx + 1))
 
     
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
           invoice_Extracted_Vendor_Data["VendorName"] = vendor_name.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["VendorName"] = None
 
 
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            invoice_Extracted_Vendor_Data["VendorAddress"] = vendor_address.content.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["VendorAddress"] = None
         
       
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
           invoice_Extracted_Vendor_Data["VendorAddressRecipient"] =   vendor_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["VendorAddressRecipient"] = None
         
 
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
           invoice_Extracted_Vendor_Data["CustomerName"] = customer_name.value
        else:
            invoice_Extracted_Vendor_Data["CustomerName"] = None
         

        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
         invoice_Extracted_Vendor_Data["CustomerId"] = customer_id.value
        else:
            invoice_Extracted_Vendor_Data["CustomerId"] = None
         

        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
         invoice_Extracted_Vendor_Data["CustomerAddress"] = customer_address.content.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["CustomerAddress"] = None
         
   
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
           invoice_Extracted_Vendor_Data["CustomerAddressRecipient"] = customer_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["CustomerAddressRecipient"] = None
        
 
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
         invoice_Extracted_Vendor_Data["InvoiceId"] = invoice_id.value
        else:
            invoice_Extracted_Vendor_Data["InvoiceId"] = None
        

        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
         formatted_date = invoice_date.value.strftime("%Y-%m-%d")
         invoice_Extracted_Vendor_Data["InvoiceDate"] = formatted_date
        else:
            invoice_Extracted_Vendor_Data["InvoiceDate"] = None
        

        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
         invoice_Extracted_Vendor_Data["InvoiceTotal"] = "{:.2f}".format(float(invoice_total.value.amount))
        else:
            invoice_Extracted_Vendor_Data["InvoiceTotal"] = None
        
 
        due_date = invoice.fields.get("DueDate")
        if due_date:
          invoice_Extracted_Vendor_Data["DueDate"] = due_date.value
        else:
            invoice_Extracted_Vendor_Data["DueDate"] = None
        

        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order: 
           invoice_Extracted_Vendor_Data["PurchaseOrder"] = purchase_order.value
        else:
            invoice_Extracted_Vendor_Data["PurchaseOrder"] = None
        

        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
           invoice_Extracted_Vendor_Data["BillingAddress"] = billing_address.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["BillingAddress"] = None
        

        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient: 
           invoice_Extracted_Vendor_Data["BillingAddressRecipient"] = billing_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["BillingAddressRecipient"] = None
        

        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
         invoice_Extracted_Vendor_Data["ShippingAddress"] = shipping_address.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["ShippingAddress"] = None
        

        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
         invoice_Extracted_Vendor_Data["ShippingAddressRecipient"] = shipping_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["ShippingAddressRecipient"] = None
        

        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            invoice_Extracted_Vendor_Data["SubTotal"] = "{:.2f}".format(float( subtotal.value.amount))
        else:
            invoice_Extracted_Vendor_Data["SubTotal"] = None
        

        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            invoice_Extracted_Vendor_Data["TotalTax"] = "{:.2f}".format(float( total_tax.value.amount))
        else:
            invoice_Extracted_Vendor_Data["TotalTax"] = None
        
 
 
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            invoice_Extracted_Vendor_Data["PreviousUnpaidBalance"] = "{:.2f}".format(float( previous_unpaid_balance.value.amount))
        else:
            invoice_Extracted_Vendor_Data["PreviousUnpaidBalance"] = None
        

 
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            invoice_Extracted_Vendor_Data["AmountDue"] = "{:.2f}".format(float( amount_due.value.amount))
        else:
            invoice_Extracted_Vendor_Data["AmountDue"] = None
        

 
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            invoice_Extracted_Vendor_Data["ServiceStartDate"] = service_start_date.value
        else:
            invoice_Extracted_Vendor_Data["ServiceStartDate"] = None
        
 
 
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            invoice_Extracted_Vendor_Data["ServiceEndDate"] = service_end_date.value
        else:
            invoice_Extracted_Vendor_Data["ServiceEndDate"] = None
        
 
 
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            invoice_Extracted_Vendor_Data["ServiceAddress"] = service_address.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["ServiceAddress"] = None
        

 
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            invoice_Extracted_Vendor_Data["ServiceAddressRecipient"] =  service_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["ServiceAddressRecipient"] = None
        


 
        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            invoice_Extracted_Vendor_Data["RemittanceAddress"] = remittance_address.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["RemittanceAddress"] = None
        


 
        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            invoice_Extracted_Vendor_Data["RemittanceAddressRecipient"] = remittance_address_recipient.value.replace('\n', '')
        else:
            invoice_Extracted_Vendor_Data["RemittanceAddressRecipient"] = None
        



    #Creating List for saving extracted Line Items
         
    invoice_Extracted_Material_Data = []   

    #Creating dictionary for multiple line item
    
    invoice_Extracted_Line_Item_Data= {}

    print("Invoice items:")
    for idx, item in enumerate(invoice.fields.get("Items").value):
       
       # print("...Item #{}".format(idx + 1))
     
     
        item_description = item.value.get("Description")
        if item_description:
            invoice_Extracted_Line_Item_Data["Description"] = item_description.value
        else:
            invoice_Extracted_Vendor_Data["Description"] = None
          
 
 
        item_quantity = item.value.get("Quantity")
        if item_quantity:
            invoice_Extracted_Line_Item_Data["Quantity"] =item_quantity.value
        else:
            invoice_Extracted_Vendor_Data["Quantity"] = None
         
 
        unit = item.value.get("Unit")
        if unit:
            invoice_Extracted_Line_Item_Data["Unit"] = unit.value
        else:
            invoice_Extracted_Vendor_Data["Unit"] = None
        

 
 
        unit_price = item.value.get("UnitPrice")
        if unit_price:
            invoice_Extracted_Line_Item_Data["UnitPrice"] = "{:.2f}".format(float( unit_price.value.amount))
        else:
            invoice_Extracted_Vendor_Data["UnitPrice"] = None
        


 
        product_code = item.value.get("ProductCode")
        if product_code:
            invoice_Extracted_Line_Item_Data["ProductCode"] = product_code.value
        else:
            invoice_Extracted_Vendor_Data["ProductCode"] = None
        


 
        item_date = item.value.get("Date")
        if item_date:
            invoice_Extracted_Line_Item_Data["Date"] = item_date.value
        else:
            invoice_Extracted_Vendor_Data["Date"] = None
        


 
        tax = item.value.get("Tax")
        if tax:
            invoice_Extracted_Line_Item_Data["Tax"] = "{:.2f}".format(float(tax.value.amount))
        else:
            invoice_Extracted_Vendor_Data["Tax"] = None
        


 
        amount = item.value.get("Amount")
        if amount:
            invoice_Extracted_Line_Item_Data["Amount"] = "{:.2f}".format(float(amount.value.amount))
        else:
            invoice_Extracted_Vendor_Data["Amount"] = None
        



        

    
        invoice_Extracted_Material_Data.append(invoice_Extracted_Line_Item_Data)
        invoice_Extracted_Line_Item_Data = {}



     # Iterate over each element with its index
    for index, value in enumerate(invoice_Extracted_Material_Data):
      
      cursor.execute("INSERT INTO Invoices_Details (UniqueId, MailId, FileName, DestinationFolder, Status, LineItemNumber, VendorName, VendorAddress, VendorAddressRecipient, CustomerName, CustomerId, CustomerAddress, CustomerAddressRecipient,InvoiceId, InvoiceDate, InvoiceTotal, DueDate, PurchaseOrder,BillingAddress, BillingAddressRecipient, ShippingAddress, ShippingAddressRecipient,SubTotal, TotalTax, PreviousUnpaidBalance, AmountDue, ServiceStartDate, ServiceEndDate, ServiceAddress, ServiceAddressRecipient,RemittanceAddress, RemittanceAddressRecipient,Description, Quantity, Unit, UnitPrice, ProductCode,Date, Tax, Amount) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                     (Unique_Id, Mail_Id, File_Name, Destination_Folder, "Success", index+1, invoice_Extracted_Vendor_Data['VendorName'], invoice_Extracted_Vendor_Data['VendorAddress'], invoice_Extracted_Vendor_Data['VendorAddressRecipient'], invoice_Extracted_Vendor_Data['CustomerName'], invoice_Extracted_Vendor_Data['CustomerId'], invoice_Extracted_Vendor_Data['CustomerAddress'], invoice_Extracted_Vendor_Data['CustomerAddressRecipient'], invoice_Extracted_Vendor_Data['InvoiceId'], invoice_Extracted_Vendor_Data['InvoiceDate'], invoice_Extracted_Vendor_Data['InvoiceTotal'], invoice_Extracted_Vendor_Data['DueDate'], invoice_Extracted_Vendor_Data['PurchaseOrder'], invoice_Extracted_Vendor_Data['BillingAddress'], invoice_Extracted_Vendor_Data['BillingAddressRecipient'],
                       invoice_Extracted_Vendor_Data['ShippingAddress'], invoice_Extracted_Vendor_Data['ShippingAddressRecipient'], invoice_Extracted_Vendor_Data['SubTotal'], invoice_Extracted_Vendor_Data['TotalTax'], invoice_Extracted_Vendor_Data['PreviousUnpaidBalance'], invoice_Extracted_Vendor_Data['AmountDue'], invoice_Extracted_Vendor_Data['ServiceStartDate'], invoice_Extracted_Vendor_Data['ServiceEndDate'], invoice_Extracted_Vendor_Data['ServiceAddress'], invoice_Extracted_Vendor_Data['ServiceAddressRecipient'], invoice_Extracted_Vendor_Data['RemittanceAddress'], invoice_Extracted_Vendor_Data['RemittanceAddressRecipient'],
                         value.get("Description",None), value.get("Quantity",None), value.get("Unit",None), value.get("UnitPrice",None), value.get("ProductCode",None), value.get("Date",None), value.get("Tax",None), value.get("Amount",None)  )) 
      
      db.commit()
      
    #  print(f"Index: {index}, Value: {value}")
        
    print("Invoice Fields Inserted successfully")
        




 
 
except HttpResponseError as e:
    print("Form recognizer service returned error:")
    print(e.message)
    print(f"Error code: {e.error.code}")
 
    # You can also print the status
    print(f"Status code: {e.response.status_code}")
 
# Success
else:
    print("Invoice analysis completed successfully. status = 200")
    print(invoice_Extracted_Vendor_Data)
    print("************************************")
    print("Final List----------")
    print(invoice_Extracted_Material_Data)  """

    
 
 
 
 
 
   
 