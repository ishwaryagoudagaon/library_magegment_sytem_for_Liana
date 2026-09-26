-- ==========================================
-- CREATE DATABASE
-- ==========================================

CREATE SCHEMA IF NOT EXISTS library;

USE library;


-- ==========================================
-- BOOKS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS books (
    isbn VARCHAR(15) NOT NULL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    genre VARCHAR(50),
    book_language VARCHAR(50),
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);


-- ==========================================
-- USERS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) not null,
    email VARCHAR(100) NOT NULL UNIQUE,
    max_loans INT NOT NULL DEFAULT 3
);


-- ==========================================
-- LOANS TABLE
-- ==========================================

CREATE TABLE IF NOT EXISTS loans (
    loan_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(15) NOT NULL,
    user_id INT NOT NULL,
    loan_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    due_date DATE NOT NULL,
    extended_due_date DATE,
    extension_count TINYINT NOT NULL DEFAULT 0,
    late_fee DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    return_date DATE,

    FOREIGN KEY (isbn)
        REFERENCES books(isbn),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

ALTER TABLE loans
ADD COLUMN fine_paid_date DATE NULL;
