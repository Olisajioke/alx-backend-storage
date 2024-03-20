-- Create the ComputeAverageWeightedScoreForUsers procedure
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;
    DECLARE average_score FLOAT DEFAULT 0;

    -- Declare cursor to iterate through users
    DECLARE users_cursor CURSOR FOR
        SELECT id FROM users;

    -- Declare continue handler for the cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN users_cursor;

    -- Start fetching rows from the cursor
    users_loop: LOOP
        -- Fetch user_id from the cursor
        FETCH users_cursor INTO user_id;

        -- Exit loop if no more rows
        IF done THEN
            LEAVE users_loop;
        END IF;

        -- Calculate the total weighted score and total weight for the current user
        SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
        INTO total_score, total_weight
        FROM corrections
        INNER JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Calculate the average weighted score for the current user
        IF total_weight > 0 THEN
            SET average_score = total_score / total_weight;
        ELSE
            SET average_score = 0;
        END IF;

        -- Update the users table with the average weighted score for the current user
        UPDATE users
        SET average_score = average_score
        WHERE id = user_id;
    END LOOP;

    -- Close the cursor
    CLOSE users_cursor;
END //

DELIMITER ;
