-- Create trigger to reset valid_email attribute when email is changed
DROP TRIGGER IF EXISTS reset_valid_email;
DELIMITER //

CREATE TRIGGER reset_valid_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        SET NEW.valid_email = 0;
    ELSE
        SET NEW.valid_email = NEW.valid_email;
    END IF;
END;
//

DELIMITER ;
