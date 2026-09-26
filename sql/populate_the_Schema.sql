-- ==========================================
-- POPULATE BOOKS
-- ==========================================

INSERT INTO books
    (isbn, title, author, genre, book_language, is_available)
VALUES
    ('9780140449136', 'The Odyssey', 'Homer', 'Epic', 'English', TRUE),
    ('9780743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'English', TRUE),
    ('9780061120084', 'To Kill a Mockingbird', 'Harper Lee', 'Classic', 'English', TRUE),
    ('9780451524935', '1984', 'George Orwell', 'Dystopian', 'English', TRUE),
    ('9780261103303', 'The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'English', TRUE),
    ('9780439023481', 'The Hunger Games', 'Suzanne Collins', 'Science Fiction', 'English', TRUE),
    ('9780132350884', 'Clean Code', 'Robert C. Martin', 'Programming', 'English', TRUE),
    ('9781491957660', 'Python Crash Course', 'Eric Matthes', 'Programming', 'English', TRUE),
    ('9784062745000', 'Norwegian Wood', 'Haruki Murakami', 'Romance', 'Japanese', TRUE),
    ('9788184001754', 'The Alchemist', 'Paulo Coelho', 'Adventure', 'English', TRUE);


-- ==========================================
-- POPULATE USERS
-- ==========================================

INSERT INTO users
    (user_name, phone_number, email, max_loans)
VALUES
    ('John Smith', '9876543210', 'john.smith@gmail.com', 5),
    ('Emma Johnson', '9876543211', 'emma.johnson@gmail.com', 5),
    ('Michael Brown', '9876543212', 'michael.brown@gmail.com', 3),
    ('Sophia Davis', '9876543213', 'sophia.davis@gmail.com', 5),
    ('Daniel Wilson', '9876543214', 'daniel.wilson@gmail.com', 4),
    ('Olivia Martinez', '9876543215', 'olivia.martinez@gmail.com', 5),
    ('James Anderson', '9876543216', 'james.anderson@gmail.com', 2),
    ('Ava Taylor', '9876543217', 'ava.taylor@gmail.com', 5),
    ('William Thomas', '9876543218', 'william.thomas@gmail.com', 3),
    ('Isabella Moore', '9876543219', 'isabella.moore@gmail.com', 5);


-- ==========================================
-- POPULATE LOANS
-- ==========================================

INSERT INTO loans
    (
        isbn,
        user_id,
        loan_date,
        due_date,
        extended_due_date,
        extension_count,
        late_fee,
        return_date
    )
VALUES
    (
        '9780140449136',
        1,
        '2026-09-01',
        '2026-09-15',
        NULL,
        0,
        0.00,
        NULL
    ),

    (
        '9780743273565',
        2,
        '2026-09-02',
        '2026-09-16',
        NULL,
        0,
        0.00,
        NULL
    ),

    (
        '9780061120084',
        3,
        '2026-08-20',
        '2026-09-03',
        '2026-09-10',
        1,
        2.50,
        NULL
    ),

    (
        '9780451524935',
        4,
        '2026-09-04',
        '2026-09-18',
        NULL,
        0,
        0.00,
        NULL
    ),

    (
        '9780261103303',
        5,
        '2026-08-25',
        '2026-09-08',
        NULL,
        0,
        5.00,
        NULL
    ),

    (
        '9780439023481',
        6,
        '2026-09-05',
        '2026-09-19',
        NULL,
        0,
        0.00,
        NULL
    ),

    (
        '9780132350884',
        7,
        '2026-08-15',
        '2026-08-29',
        NULL,
        0,
        10.00,
        '2026-08-28'
    ),

    (
        '9781491957660',
        8,
        '2026-09-06',
        '2026-09-20',
        NULL,
        0,
        0.00,
        NULL
    ),

    (
        '9784062745000',
        9,
        '2026-08-10',
        '2026-08-24',
        NULL,
        0,
        7.50,
        '2026-08-23'
    ),

    (
        '9788184001754',
        10,
        '2026-09-07',
        '2026-09-21',
        NULL,
        0,
        0.00,
        NULL
    );


-- ==========================================
-- CHECK THE DATA
-- ==========================================

SELECT * FROM books;

SELECT * FROM users;

SELECT * FROM loans;