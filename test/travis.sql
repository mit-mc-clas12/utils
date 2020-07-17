# Create Testuser

# Create DB
CREATE DATABASE IF NOT EXISTS `CLAS12OCR`;

CREATE USER 'dev'@'localhost' IDENTIFIED BY 'dev';
GRANT ALL ON CLAS12OCR.* TO 'dev'@'localhost';