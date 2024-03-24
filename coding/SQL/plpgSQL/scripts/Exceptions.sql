-- Handling Exceptions
DO
$$
DECLARE
	customer record;
	id_of_customer INT = 10000;
BEGIN
	SELECT * INTO customer
	FROM customers
	WHERE customer_id = id_of_customer;
  -- Make sure that a customer exists
	ASSERT customer IS NOT NULL;
		raise notice 'Selected Customer: %', customer.first_name;
  -- Otherwise henerate an eeror
	EXCEPTION WHEN assert_failure THEN
		raise EXCEPTION 'Customer Wth ID % Not Exists!', id_of_customer
			USING hint = 'Try Another ID';
END $$;
