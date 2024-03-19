-- CASE Expression
DO $$
DECLARE
	customer record;
BEGIN
SELECT first_name, last_name,
	CASE
		WHEN age BETWEEN 0 AND 10 THEN 'Kinds' -- no need to close with semi colon
		WHEN age BETWEEN 11 AND 18 THEN 'Teenagers'
		WHEN age BETWEEN 19 AND 30 THEN 'Adult'
		ELSE 'Aged'
	END as age_category
INTO customer
FROM customers
WHERE customer_id = 77;

raise notice 'Selected Customer Belongs to a % Category!', customer.age_category;

END$$;

-- Simple CASE Example 
DO $$
DECLARE
	customer record;
	renamed_gender customers.gender%type;
BEGIN
	SELECT * INTO customer
	FROM customers 
	WHERE customer_id = 88;
	
	CASE customer.gender
		WHEN 'Female' THEN renamed_gender = 'Woman'; -- each WHEN block must be closed with semi colon
		ELSE renamed_gender = 'Man'; -- ELSE must be closed with semi colon
	END CASE; --case must be closed with semi colon
	
	raise notice 'Selected Customer is a %', renamed_gender;
END $$;
	
-- Searched CASE Example
DO $$
DECLARE
	customer record;
	customer_category VARCHAR(15);
BEGIN
	SELECT * INTO customer
	FROM customers 
	WHERE customer_id = 99;
	
	CASE 
		WHEN customer.age BETWEEN 0 AND 10 THEN customer_category = 'Kinds';
		WHEN customer.age BETWEEN 11 AND 18 THEN customer_category = 'Teenagers';
		WHEN customer.age BETWEEN 19 AND 30 THEN customer_category = 'Adult';
		ELSE customer_category = 'Aged';
	END CASE;
	
	raise notice 'Selected Customer Belongs to a % Category', customer_category;
END $$;