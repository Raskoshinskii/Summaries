-- Procedure Creation
CREATE OR REPLACE PROCEDURE money_transfer(sender_id INT, recipient_id INT, amount DECIMAL)
-- Procedures don't return any values
LANGUAGE plpgsql
AS 
$$
BEGIN
    -- Money Substraction
    UPDATE accounts
    SET balance = balance - amount
    WHERE id = sender_id;

    -- Money Obtaining
    UPDATE accounts
    SET balance = balance + amount
    WHERE id = recipient_id;

    COMMIT;
END;
$$

-- Procedures are called:
call money_transfer(sender_id := 1, recipient_id := 3, amount := 5000)