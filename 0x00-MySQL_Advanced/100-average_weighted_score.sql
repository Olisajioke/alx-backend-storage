-- Create the ComputeAverageWeightedScoreForUser procedure
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the total weighted score and total weight
    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO total_score, total_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Calculate the average weighted score
    DECLARE average_score FLOAT DEFAULT 0;
    IF total_weight > 0 THEN
        SET average_score = total_score / total_weight;
    END IF;

    -- Update the users table with the average weighted score
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //

DELIMITER ;
