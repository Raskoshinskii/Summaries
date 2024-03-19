-- Simple WHILE
DO $$
DECLARE
	counter SMALLINT = 0;
BEGIN
WHILE counter != 10
	LOOP
		raise notice 'Current Counter Is %', counter;
		counter = counter + 1;
	END LOOP;
END $$;

--Simple FOR LOOP
DO $$
BEGIN
FOR i IN 0..10
	LOOP
		raise notice 'Current Counter Is %', i;
	END LOOP;
END $$;

-- FOR LOOP WITH REVERSE ORDER AND DIFFERENT STEP SIZE
DO $$
BEGIN
FOR i in reverse 10..0 BY 2
	LOOP
		raise notice 'Current Counter Is %', i;
	END LOOP;
END $$;

-- ITERATING OVER A QUERY
DO $$
DECLARE
	customer record;
BEGIN
	FOR customer IN
		SELECT first_name, gender, age, city
		FROM customers
		ORDER BY age DESC, first_name
		LIMIT 7
	LOOP
		raise notice 'Name: % Gender: % Age: % City: %',
			customer.first_name,
			customer.gender,
			customer.age,
			customer.city;
	END LOOP;
END $$;

-- FOR LOOP in Dynamic Query
DO $$
DECLARE
	-- Declare variables that will be changing the dynamic query
	type_of_sorting SMALLINT = 1;
	number_of_records SMALLINT = 5;
	customer record;
	query TEXT;
BEGIN
	query = 'SELECT first_name, age, city
					 FROM customers';

  IF type_of_sorting = 0 THEN
		query = query || ' ORDER BY age DESC';
	ELSIF type_of_sorting = 1 THEN
		query = query || ' ORDER BY age';
	ELSE
		raise exception 'Invalid Type Of Sorting!'
			using hint = 'Type Of Sorting Can Be Either 0 Or 1';
	END IF;

	query = query || ' LIMIT $1';

	FOR customer IN EXECUTE query USING number_of_records
	LOOP
		raise notice 'Customer Name: % Age: % City: %', customer.first_name, customer.age, customer.city;
	END LOOP;

END $$;
