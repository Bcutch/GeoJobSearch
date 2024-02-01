USE template_db;

CREATE TABLE IF NOT EXISTS job (
    id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    url VARCHAR(255) NOT NULL,
    salary INT NOT NULL,
    field VARCHAR(255) NOT NULL,
    is_remote BOOLEAN NOT NULL DEFAULT FALSE,
    latitude DECIMAL(11,8) NOT NULL,
    longitude DECIMAL(11,8) NOT NULL
);
