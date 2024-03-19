DO $$
DECLARE
	i SMALLINT = 10;
BEGIN
	LOOP
		i = i - 1;
		EXIT WHEN i < 0;
		CONTINUE WHEN mod(i,2) != 0;
		raise notice 'Even NUmber Is %', i;
	END LOOP;
END $$;
