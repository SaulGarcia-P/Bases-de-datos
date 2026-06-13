
CREATE TABLE customers (
	`CustomerID` FLOAT(53), 
	`Country` TEXT
)

;


CREATE TABLE products (
	`StockCode` TEXT, 
	`Description` TEXT, 
	`UnitPrice` FLOAT(53)
)

;


CREATE TABLE invoices (
	`InvoiceNo` TEXT, 
	`InvoiceDate` TEXT, 
	`CustomerID` FLOAT(53)
)

;


CREATE TABLE invoice_details (
	`InvoiceNo` TEXT, 
	`StockCode` TEXT, 
	`Quantity` BIGINT
)

;

