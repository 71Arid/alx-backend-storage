-- stored procedure to compute avarage score for user
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;
	DECLARE total_score INT;
	DECLARE counter INT;

	SELECT SUM(score), COUNT(score) INTO total_score, counter
	FROM corrections
	WHERE corrections.user_id = user_id;

	IF counter > 0 THEN
		SET avg_score = total_score / counter;
	ELSE
		SET avg_score = 0;
	END IF;

	UPDATE users
	SET average_score = avg_score
	WHERE id = user_id;
END$$
DELIMITER ;
