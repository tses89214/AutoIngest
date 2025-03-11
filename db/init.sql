CREATE DATABASE IF NOT EXISTS data_ingestion;

USE data_ingestion;

DROP TABLE IF EXISTS `expect_schema`;
CREATE TABLE expect_schema (
  `column` VARCHAR(255),
  `column_order` INT,
  `data_type` VARCHAR(255),
  `table` VARCHAR(255),
   PRIMARY KEY (`column`, `table`)
);

INSERT INTO expect_schema (`column`,`column_order`, `data_type`, `table`) VALUES
('id', 1,'int', 'table1'),
('name', 2, 'str', 'table1'),
('age', 3, 'int', 'table1'),
('date', 1, 'timestamp', 'table2'),
('customer_id', 2, 'str', 'table2'),
('amount', 3, 'float', 'table2');

-- Create the read-only user
CREATE USER 'readonlyuser'@'%' IDENTIFIED BY 'readonlypassword';

-- Grant read-only privileges to the user on the specified database
GRANT SELECT ON *.* TO 'readonlyuser'@'%';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
