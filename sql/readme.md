# SQL Files

This folder contains the SQL scripts used to create and manage the MySQL database for the Liana's Library Management System.

## Files

- **`schema_creation.sql`** — Creates the `library` database and the `books`, `users`, and `loans` tables, including their primary keys, foreign keys, and constraints.
- **`populate_the_schema.sql`** — Contains SQL statements used to insert or update samples in library data.

## Database Structure

The database contains three main tables:

- **Books** — stores book information and availability.
- **Users** — stores borrower information and loan allowance.
- **Loans** — stores borrowing, due-date, extension, return, and fine information.

## Usage

Run the schema SQL file in MySQL first to create the database and tables. The data update script can then be used to add or modify library data.

The SQL files provide the database foundation used by the Streamlit application.
