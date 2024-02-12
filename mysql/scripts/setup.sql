USE template_db;

CREATE TABLE IF NOT EXISTS job 
(
    id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
    title VARCHAR(255) ,
    company VARCHAR(255) ,
    location VARCHAR(255) ,
    description TEXT ,
    url VARCHAR(1023) ,
    salary INT ,
    field VARCHAR(255) ,
    is_remote BOOLEAN  DEFAULT FALSE,
    latitude DECIMAL(11,8) ,
    longitude DECIMAL(11,8) 
);
