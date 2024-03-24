-- get lifespan of bands with style glam rock
DELIMITER $$
CREATE FUNCTION lifespan(a INT, b INT)
RETURNS INT
BEGIN
	DECLARE result INT;
	IF b IS NULL THEN
		SET b = 2022;
	END IF;
	SET result = b - a;
	RETURN result;
END $$
DELIMITER ;
SELECT band_name, lifespan(formed, split) AS lifespan
FROM metal_bands
WHERE style LIKE "%Glam rock%";
