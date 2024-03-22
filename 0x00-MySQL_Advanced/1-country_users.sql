-- script creates a user table with the following criteria
CREATE TABLE IF NOT EXISTS users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(255) UNIQUE NOT NULL,
	name VARCHAR(255),
	country ENUM('US','CO','TN') NOT NULL DEFAULT 'US'
);
