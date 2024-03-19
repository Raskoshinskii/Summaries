--ASSERT EXAMPLE
DO $$
DECLARE
	selected_customer customers%rowtype;
BEGIN
	SELECT * INTO selected_customer
	FROM customers
	WHERE customer_id = 10;

	assert selected_customer.age > 40, 'Customer Age Must be more than 40!!!';
END $$;


-- Examples of raise notice, info and warning
DO $$
DECLARE
	selected_customer customers%rowtype;
BEGIN

	raise warning 'Data Retrieving Has Been Started!';

	SELECT * INTO selected_customer
	FROM customers
	WHERE customer_id = 10;

	raise info 'Selected Customer %', selected_customer.first_name;
	raise notice 'Data Has Been Successfully Retrieved!';
END $$;


-- Variables Changing
DO $$
DECLARE
	selected_customer customers%rowtype;
BEGIN
	SELECT * INTO selected_customer
	FROM customers
	WHERE customer_id = 11;
	-- Original Age
	raise info 'Customer Age %', selected_customer.age;

	--Substract 10 from the Age
	selected_customer.age = selected_customer.age - 10;
	raise info 'New Customer Age %', selected_customer.age;
END $$;
