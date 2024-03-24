-- calculate weighted average
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
	DECLARE weighted_score INT DEFAULT 0;
	DECLARE total_weight INT DEFAULT 0;

	SELECT SUM(corrections.score * projects.weight), SUM(projects.weight) INTO weighted_score, total_weight
	FROM corrections
	INNER JOIN projects
	ON corrections.project_id = projects.id
	WHERE corrections.user_id = user_id;

	IF total_weight = 0 THEN
		UPDATE users
		SET users.average_score = 0
		WHERE users.id = user_id;
	ELSE
		UPDATE users
		SET users.average_score = weighted_score / total_weight
		WHERE users.id = user_id;
	END IF;
END$$
DELIMITER ;
