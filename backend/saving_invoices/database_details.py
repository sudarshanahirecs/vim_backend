import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="vim"
)

cursor = db.cursor()

#cursor.execute("CREATE TABLE Invoice_Master(SrNo INT AUTO_INCREMENT PRIMARY KEY, UniqueId VARCHAR(100), MailId VARCHAR(30), FileName VARCHAR(50), DestinationFolder VARCHAR(100), Status VARCHAR(20))")



#cursor.execute("CREATE TABLE Invoice_Details (SrNo INT AUTO_INCREMENT PRIMARY KEY, UniqueId VARCHAR(100), MailId VARCHAR(30), FileName VARCHAR(200), DestinationFolder VARCHAR(200), Status VARCHAR(50),LineItemNumber INT,VendorName VARCHAR(255),VendorAddress VARCHAR(500),VendorAddressRecipient VARCHAR(500),CustomerName VARCHAR(500),CustomerId VARCHAR(100),CustomerAddress VARCHAR(500),CustomerAddressRecipient VARCHAR(500),InvoiceId VARCHAR(100),InvoiceDate DATE,InvoiceTotal DECIMAL(10, 2), DueDate DATE,PurchaseOrder VARCHAR(200),BillingAddress VARCHAR(500), BillingAddressRecipient VARCHAR(500), ShippingAddress VARCHAR(500), ShippingAddressRecipient VARCHAR(500), SubTotal DECIMAL(10, 2), TotalTax DECIMAL(10, 2), PreviousUnpaidBalance DECIMAL(10, 2), AmountDue DECIMAL(10, 2), ServiceStartDate DATE, ServiceEndDate DATE, ServiceAddress VARCHAR(500), ServiceAddressRecipient VARCHAR(500), RemittanceAddress VARCHAR(500), RemittanceAddressRecipient VARCHAR(500), Description TEXT, Quantity DECIMAL(10, 2), Unit VARCHAR(100), UnitPrice DECIMAL(10, 2), ProductCode VARCHAR(100), Date DATE, Tax DECIMAL(10, 2), Amount DECIMAL(10, 2))")

#cursor.execute("DELETE FROM Invoice_Master WHERE ")

#cursor.execute("UPDATE Invoice_Master SET Status='Pending' WHERE SrNo IN (8,9)")

cursor.execute("UPDATE Invoice_Details SET Status='Pending' WHERE SrNo IN (60,61,62)")

#cursor.execute("ALTER TABLE Invoice_Details MODIFY COLUMN VendorAddress TEXT, MODIFY COLUMN VendorAddressRecipient TEXT, MODIFY COLUMN CustomerAddress TEXT, MODIFY COLUMN CustomerAddressRecipient TEXT, MODIFY COLUMN BillingAddress TEXT, MODIFY COLUMN BillingAddressRecipient TEXT, MODIFY COLUMN ShippingAddress TEXT, MODIFY COLUMN ShippingAddressRecipient TEXT, MODIFY COLUMN ServiceAddress TEXT, MODIFY COLUMN ServiceAddressRecipient TEXT, MODIFY COLUMN RemittanceAddress TEXT, MODIFY COLUMN RemittanceAddressRecipient TEXT")

db.commit()