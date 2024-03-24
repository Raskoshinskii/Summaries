-- SIMPLE LOOP Example
DO $$
DECLARE
	idx SMALLINT = 0; -- Counter
	n SMALLINT = 23; -- Element of fibonacci sequence to be calculated
	a INT = 0; -- First element of fibonacci sequence
	b INT = 1; -- The second element of fibonacci sequence
	res INT = 0; -- The result variable
BEGIN
	IF n < 1
		THEN res = 0;
	END IF;

	LOOP
		EXIT WHEN idx = n;
		idx = idx + 1;
		SELECT b, a+b INTO a, b;
	END LOOP;

	res = a; -- Final Output

	-- Add Beauty
	IF n = 0 THEN
		raise notice 'Zero Element Of Fibonacci Sequence Is %', res;
	ELSIF n = 1 THEN
		raise notice 'The First Element Of Fibonacci Sequence Is %', res;
	ELSIF n = 2 THEN
		raise notice 'The Second Element Of Fibonacci Sequence Is %', res;
	ELSIF n = 3 THEN
		raise notice 'The Third Element Of Fibonacci Sequence Is %', res;
	ELSE
		raise notice 'The %th Element Of Fibonacci Sequence Is %', n, res;
	END IF;

END $$;
