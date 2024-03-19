USE template_db;

CREATE TABLE IF NOT EXISTS job 
(
    id INT AUTO_INCREMENT COMMENT 'Primary Key' PRIMARY KEY,
    title VARCHAR(255) DEFAULT "TITLE",
    company VARCHAR(255) DEFAULT "COMPANY",
    location VARCHAR(255) DEFAULT "GUELPH",
    description TEXT DEFAULT "Description of the Job",
    url VARCHAR(2083) DEFAULT "www.indeed.com",         -- was: url VARCHAR(768) UNIQUE, changed back because links larger than 768 were found
    salary INT DEFAULT 0,
    field VARCHAR(255) DEFAULT "Job field",
    is_remote BOOLEAN  DEFAULT FALSE,
    latitude DECIMAL(11,8)  DEFAULT 80.2482,
    longitude DECIMAL(11,8) DEFAULT 43.5448
);
