DO
$$
DECLARE
-- Each row must have ;
	city_name customers.city%type; -- Type of a variable can be defined using a data type of a column from another table
	count_city SMALLINT = 0;
BEGIN
	-- First Command ( each command must be finished with ;)
	SELECT c.city as city_name, count(c.city) INTO city_name, count_city
	FROM customers c
	GROUP BY c.city
	HAVING count(c.city) > 1
	ORDER BY city_name
	LIMIT 1
	OFFSET 1;
	-- The second command
	raise notice 'Found City: % Count_City: %', city_name, count_city;
END;
$$

-- Saving a row returned by a SELECT INTO operator
DO
$$
DECLARE
	selected_customer customers%rowtype; --using %rowtype
	sel_cust record; -- using record type
BEGIN
	SELECT * INTO selected_customer
	FROM customers c 
	WHERE c.customer_id = 23;

	raise notice 'Customer Name: % Gender: % City: %',
					selected_customer.first_name,
					selected_customer.gender,
					selected_customer.city;

	SELECT * INTO sel_cust
	FROM customers c
	WHERE c.customer_id = 100;

	raise notice 'Customer Name: % Gender: % City: %',
					sel_cust.first_name,
					sel_cust.gender,
					sel_cust.city;
END;
$$
