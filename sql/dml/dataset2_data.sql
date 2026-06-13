-- Inserciones de ejemplo para la tabla: customers
INSERT INTO customers VALUES ('17850.0', 'United Kingdom');
INSERT INTO customers VALUES ('13047.0', 'United Kingdom');
INSERT INTO customers VALUES ('12583.0', 'France');
INSERT INTO customers VALUES ('13748.0', 'United Kingdom');
INSERT INTO customers VALUES ('15100.0', 'United Kingdom');

-- Inserciones de ejemplo para la tabla: products
INSERT INTO products VALUES ('85123A', 'WHITE HANGING HEART T-LIGHT HOLDER', '2.55');
INSERT INTO products VALUES ('71053', 'WHITE METAL LANTERN', '3.39');
INSERT INTO products VALUES ('84406B', 'CREAM CUPID HEARTS COAT HANGER', '2.75');
INSERT INTO products VALUES ('84029G', 'KNITTED UNION FLAG HOT WATER BOTTLE', '3.39');
INSERT INTO products VALUES ('84029E', 'RED WOOLLY HOTTIE WHITE HEART.', '3.39');

-- Inserciones de ejemplo para la tabla: invoices
INSERT INTO invoices VALUES ('536365', '12/1/2010 8:26', '17850.0');
INSERT INTO invoices VALUES ('536366', '12/1/2010 8:28', '17850.0');
INSERT INTO invoices VALUES ('536367', '12/1/2010 8:34', '13047.0');
INSERT INTO invoices VALUES ('536368', '12/1/2010 8:34', '13047.0');
INSERT INTO invoices VALUES ('536369', '12/1/2010 8:35', '13047.0');

-- Inserciones de ejemplo para la tabla: invoice_details
INSERT INTO invoice_details VALUES ('536365', '21730', '6');
INSERT INTO invoice_details VALUES ('536365', '22752', '2');
INSERT INTO invoice_details VALUES ('536365', '71053', '6');
INSERT INTO invoice_details VALUES ('536365', '84029E', '6');
INSERT INTO invoice_details VALUES ('536365', '84029G', '6');

