-- Creation of Bounded Cursors
DO $$
DECLARE
    full_name TEXT DEFAULT '';
    customer_age INT = 20;
    records_to_show INT = 10;
    customer record;
    -- Normally, Cursors are defined in DECLAE block
    -- Let's define a cursor that will store all customers (all rows will be stored in cur_customers)
    cur_customers CURSOR FOR
        SELECT * FROM customers;
    -- Define a cursor that will store customers whose age less than 20.
    cur_teen_customers CURSOR (customer_age INT, n INT) FOR
        SELECT * FROM customers
        WHERE age < customer_age
		LIMIT n;
BEGIN
    -- Open the cursor
    OPEN cur_teen_customers(customer_age, records_to_show);
    -- Iterate over the cursor
    LOOP
        -- Each cursor record will be saved into variable customer
        FETCH cur_teen_customers INTO customer;
        -- When there is no any rows left, exit from the loop
        EXIT WHEN NOT FOUND;
        full_name = customer.first_name || ' ' || customer.last_name;
				raise notice 'Customer Full Name: %', full_name;
    END LOOP;

    -- Cursor must be closed
    CLOSE cur_teen_customers;
END;
$$

-- Creation of an Unbounded Cursor
CREATE OR REPLACE FUNCTION get_aged_customers (customer_age INT DEFAULT 50)
RETURNS TABLE (
    full_name VARCHAR,
    customer_gender VARCHAR(10),
    customer_city VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
DECLARE
    -- Declare only a cursor without a query (i.e. define an unbounded cursor)
    customer_cur refcursor;
    -- This will be a dynamic query (i.e. it has a parameter which will be set later)
    query VARCHAR = 'SELECT * FROM customers WHERE age > $1';
    customer record;
BEGIN
    -- Open a cursor and bind it to a dynamic query
    OPEN customer_cur FOR EXECUTE query USING customer_age;
    LOOP
        FETCH customer_cur INTO customer;
        EXIT WHEN NOT FOUND;

        full_name = customer.first_name || ' ' || customer.last_name;
        customer_gender = LOWER(customer.gender);
        customer_age = customer.age;
        customer_city = UPPER(customer.city);
    RETURN NEXT;
    END LOOP;
END;
$$

SELECT * FROM get_aged_customers ();

-- Iterating over a cursor using FOR
DO
$$
DECLARE
  -- Create a bounded cursor
	customers_cur CURSOR FOR
		SELECT *
	FROM customers
	ORDER BY first_name
	LIMIT 10;
	category VARCHAR (10);
BEGIN
  -- This time create a table to store values from a cursor
	CREATE TABLE IF NOT EXISTS res_table (
		full_name TEXT,
		category VARCHAR(10)
		);

  -- Iterating over a cursor. Now variable customer will have a record type and can access all columns of a cursor
	FOR customer IN customers_cur
	LOOP
		CASE
			WHEN customer.age BETWEEN 0 AND 10 THEN category = 'Kids';
			WHEN customer.age BETWEEN 11 AND 20 THEN category = 'Teens';
			ELSE category = 'Aged';
		END CASE;

		INSERT INTO res_table (full_name, category) VALUES
      -- Two options of inserting a value
			(customer.first_name || ' ' || customer.last_name, category);
	END LOOP;
END $$;

-- Cursor Moving
DO
$$
DECLARE
	customer record;
	my_cursor CURSOR FOR
		SELECT customer_id, first_name
		FROM customers
		WHERE age < 25
		ORDER BY age DESC
		LIMIT 10;
BEGIN
	OPEN my_cursor;

	-- By default FETCH NEXT is used
	FETCH my_cursor INTO customer;
		raise notice '%', customer;

	-- Select the last row from a cursor
	FETCH LAST FROM my_cursor INTO customer;
		raise notice '%', customer;

	-- Select the first row from a cursor
	FETCH FIRST FROM my_cursor INTO customer;
		raise notice '%', customer;

	-- Moving a cursor on 5 rows forward
	MOVE FORWARD 5 FROM my_cursor;
	FETCH my_cursor INTO customer;
		raise notice '%', customer;

	-- Moving a cursor on 3 rows backward
	MOVE BACKWARD 3 FROM my_cursor;
	FETCH my_cursor INTO customer;
		raise notice '%', customer;

	-- Can set a relative position (e.g. -2 means on 2 rows backward)
	MOVE RELATIVE -2 FROM my_cursor;
	FETCH my_cursor INTO customer;
		raise notice '%', customer;

	CLOSE my_cursor;
END $$;
