-- Simple IF Example
DO $$
DECLARE
	customer customers%rowtype;
	cust_id customers.customer_id%type = 7777;
BEGIN
	SELECT * INTO customer
	FROM customers c
	WHERE c.customer_id = cust_id;

	IF NOT FOUND THEN
		raise warning 'Customer with id % not found!', cust_id;
	END IF;
END $$;

-- IF-ELSE Example
DO $$
DECLARE
	customer customers%rowtype;
	customer_age customers.age%type = 30;
	cust_id customers.customer_id%type = 3;
BEGIN
	SELECT * INTO customer
	FROM customers
	WHERE age < customer_age AND customer_id = cust_id;

	IF FOUND THEN
		raise notice 'There is such customer!';
	ELSE
		raise notice 'No such customer!';
	END IF;

END $$;

-- IF-ELSIF-ELSE Example
DO $$
DECLARE
	customer customers%rowtype;
	cust_id customers.customer_id%type = 100;
BEGIN
	SELECT * INTO customer
	FROM customers
	WHERE customer_id = cust_id;

	IF NOT FOUND THEN
		raise notice 'Such Customer Not Found!';
	ELSIF customer.age BETWEEN 0 AND 10 THEN
		raise notice '% is a kid. Age %', customer.first_name,customer.age;
	ELSIF customer.age BETWEEN 11 AND 20 THEN
		raise notice '% is a teenager. Age %', customer.first_name, customer.age;
	ELSE
		raise notice '% is old. Age %', customer.first_name, customer.age;
	END IF;

END $$;
