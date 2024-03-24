-- Simple Function Creation
CREATE OR REPLACE FUNCTION number_of_customers_in_cluster(min_age INT, max_age INT)
RETURNS INT
LANGUAGE plpgsql
AS
$$
DECLARE
    number_of_customers SMALLINT;
BEGIN
    SELECT COUNT(*) INTO number_of_customers
	FROM customers 
    WHERE age BETWEEN min_age AND max_age;
	
	RETURN number_of_customers;
END;
$$

-- Function Execution Options 
SELECT number_of_customers_in_cluster(10,19);
SELECT number_of_customers_in_cluster(min_age := 10, max_age := 19);
SELECT number_of_customers_in_cluster(min_age => 10, max_age => 19);

-- Function Parameters Mode (By default all parameters have IN mode)
-- OUT MODE:
CREATE OR REPLACE FUNCTION customer_statistics ( 
	OUT avg_customer_age INT, 
	OUT max_first_name VARCHAR(50), 
	OUT min_city_name VARCHAR(50) )
LANGUAGE plpgsql
-- No need to define return type due to OUT parameters
AS
$$
BEGIN
	SELECT round(AVG(age)), MAX(first_name), MIN(city) INTO
		avg_customer_age, max_first_name, min_city_name
	FROM customers;
-- No need for return operator as the function has OUT parameters that will be returned automatically
END;
$$

-- This option returns record 
SELECT customer_statistics();

-- This option returns columns
SELECT * FROM customer_statistics();

-- INOUT MODE
CREATE OR REPLACE FUNCTION swap_numbers(INOUT a INT, INOUT b INT)
LANGUAGE plpgsql
AS
$$
BEGIN
    SELECT a, b INTO b, a;
END;
$$

SELECT * FROM swap_numbers(10,5);

-- Function Returning a Table
CREATE OR REPLACE FUNCTION get_customer(pattern_name TEXT)
RETURNS TABLE (
    customer_name VARCHAR(50),
    customer_age INT
)
LANGUAGE plpgsql
AS
$$
-- As it returns a table no need to define any variables
BEGIN
    RETURN QUERY
        SELECT first_name, age
        FROM customers
        WHERE first_name ILIKE pattern_name;
END;
$$

SELECT * FROM get_customer(pattern_name := 'a%');

-- Processing of a Returning Table
CREATE OR REPLACE FUNCTION process_customer(pattern_name TEXT)
RETURNS TABLE (
    customer_name VARCHAR(25),
    customer_gender VARCHAR(10),
    customer_age VARCHAR(10),
    customer_city VARCHAR(50)
)
LANGUAGE plpgsql
AS
$$
DECLARE
    customer record;
BEGIN
    -- Making Processing of a Table
    FOR customer IN (
        SELECT first_name, age, gender, city
        FROM customers
        WHERE first_name ILIKE pattern_name
    )
    LOOP
        -- Make each name in upper case 
        customer_name = UPPER(customer.first_name);
        -- Change gender name
        IF customer.gender = 'Male' THEN
            customer_gender = 'Man';
        ELSIF
            customer_gender = 'Woman';
        END IF;
        -- Make Classification Depending on Customer's Age
        IF customer.age BETWEEN 0 AND 10 THEN
            customer_age = 'Kids';
        ELSIF customer.age BETWEEN 11 AND 19 THEN
            customer_age = 'Teenagers';
        ELSE
            customer_age = 'Aged';
        END IF;
        -- Make City Lower case
        customer_city = LOWER(customer.city);
    -- To return each processed record, we use RETURN NEXT
    RETURN NEXT;
    END LOOP;
END;

SELECT * FROM process_customer(pattern_name := '%a');

-- Exception Handling 
-- Let's handle an error when a record doesn't exist
CREATE OR REPLACE FUNCTION find_not_existing_customer(id_of_customer INT)
RETURNS VARCHAR(50)
LANGUAGE plpgsql
AS
$$
DECLARE
    customer_name VARCHAR(50);
BEGIN
    SELECT first_name INTO customer_name
    FROM customers 
    WHERE customer_id = id_of_customer;
    -- Catching an Exception here
		IF NOT FOUND THEN
			raise exception 'Customer With Id % Not Found', id_of_customer
				USING hint = 'Check Customer Id!';
		ELSE
			RETURN customer_name;
		END IF;
END;
$$