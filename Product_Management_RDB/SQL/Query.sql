-- Query to create Database 
CREATE DATABASE product_management;
USE product_management;


-- Query to create Tables 

CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE plant_brand (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(255)
);

CREATE TABLE supplier (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100),
    brand_id INT,
    supplier-id INT,
    FOREIGN KEY (plant_id) REFERENCES plant_brand(id)
);

CREATE TABLE consumer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(20),
    email VARCHAR(100),
    password VARCHAR(255) NOT NULL
);

CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category_id INT,
    cost DECIMAL(10,2),
    version VARCHAR(20),
    description TEXT,
    plant_brand_id INT, 
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES supplier(id);
    FOREIGN KEY (category_id) REFERENCES category(id),
    FOREIGN KEY (brand_id) REFERENCES plant_brand(id)
);

CREATE TABLE subproduct (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20),
    description TEXT,
    product_id INT,
    FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'consumer', 'supplier') NOT NULL,
    contact VARCHAR(20),
    plant_id INT NULL,
    FOREIGN KEY (plant_id) REFERENCES plant_brand(id)
);
