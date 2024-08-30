-- Create and Setup a database for HealthPixel Project

CREATE DATABASE IF NOT EXISTS healthpixel_db;
CREATE USER IF NOT EXISTS 'healthpixel'@'localhost' IDENTIFIED BY 'healthpixel_pwd';
GRANT ALL PRIVILEGES ON `healthpixel_db`.* TO 'healthpixel'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'healthpixel'@'localhost';
FLUSH PRIVILEGES;