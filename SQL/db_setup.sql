CREATE DATABASE TKE_Garage;
USE TKE_Garage;

CREATE TABLE TKE_Member (
  scroll_number INT PRIMARY KEY,
  name VARCHAR(255),
  tool_checked_out INT
);

CREATE TABLE House_Manager (
  scroll_number INT PRIMARY KEY,
  name VARCHAR(225),
  phone_number VARCHAR(225),
  email VARCHAR(225)
);

CREATE TABLE Tools (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  last_user INT,
  location VARCHAR(255),
  last_returned DATE,
  quality VARCHAR(255),
  last_taken DATE,
  FOREIGN KEY (last_user) REFERENCES TKE_Member (scroll_number)
);

ALTER TABLE TKE_Member
ADD CONSTRAINT TKE_Member_ibfk_1
FOREIGN KEY (tool_checked_out) REFERENCES Tools (id);

CREATE TABLE Garage (
  last_cleaned DATE
);

CREATE TABLE Tool_Wishlist (
	name VARCHAR(225),
    estimated_price INT,
    submitted_by INT,
    FOREIGN KEY (submitted_by) REFERENCES TKE_Member (scroll_number)
);
