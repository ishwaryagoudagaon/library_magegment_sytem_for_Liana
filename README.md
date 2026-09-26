# Liana's Library

A simple library management system built to turn an informal book-lending process into a structured workflow for tracking books, borrowers, and loans.

## Business Case

Liana was informally lending books to people she knew, making it easy to lose track of who had a book, when it was due, and whether a book was currently available.

This system provides a structured lending workflow with book availability tracking, borrower management, automatic due-date calculation, loan extensions, return tracking, and automatic late-fee calculation.

## Features

- **Dashboard** — view total books, total users, active loans, and overdue loans.
- **Books** — add, search, update, and delete books, with real-time availability tracking.
- **Users** — manage borrowers including name, phone number, email, and maximum loan allowance.
- **Loans** — create, extend, and return book loans.
- **Automatic Due Dates** — the due date is automatically calculated as 20 days after the loan date.
- **Loan Extensions** — active loans can be extended by 10 days, with a maximum of 2 extensions.
- **Overdue Detection** — active loans are automatically checked against their effective due date.
- **Late Fees** — overdue loans automatically accumulate a late fee of $0.25 per day.
- **Returning Book** — returning a book updates the loan, makes the book available again, and restores the user's loan allowance.
- **Fine Payment Tracking** — the system records the date when an overdue fine is paid.

## Tech Stack

| Layer | Technology |
| ----------------- | ----------------- |
| Frontend / App | Streamlit |
| Database | MySQL |
| Database Access | SQLAlchemy + PyMySQL |
| Data Handling | pandas |
| Environment Management | Conda |

## Project Structure

The application follows a modular structure. `app.py` handles the main Streamlit application and page navigation, while the CRUD operations are separated into individual modules.

```text
library/

├── notebooks/
|   ├──CRUD_library.ipynb
|   ├──python_sql.ipynb
|   ├──readme.md
├── sql_files/
|   ├──schema_creation.sql
|   ├──populate_the_Schema.sql
|   ├──readme.md
├── src/
│   ├── app.py
│   ├── create.py
│   ├── read.py
│   ├── update.py
│   ├── delete.py
│   ├──readme.md
├── environment.yml
├── readme.md
└── .gitignore.txt


## Future Work

The system currently provides the core functionality for managing books, users, and loans. Future improvements could include:

- **Book Reservations**: Allow users to reserve books that are currently unavailable.
- **Email Notifications**: Send automatic reminders for upcoming and overdue books.
- **Advanced Analytics**: Analyse borrowing patterns, popular books, genres, overdue loans, and late fees.
- **Advanced Search**: Add filtering by title, author, genre, language, ISBN, and availability.
- **Reporting**: Generate downloadable reports for books, users, loans, overdue items, and fines.
- **Authentication**: Add secure user login and role-based access control.
- **Book Recommendations**: Recommend books based on previous borrowing history.
- **Automated Testing**: Add unit and integration tests for the main database operations.
- **Deployment**: Deploy the application online for remote access.
- **Mobile-Friendly Design**: Improve the interface for tablets and mobile devices.

With additional historical data, the system could also be used to investigate borrowing trends, popular genres, frequently borrowed books, overdue patterns, loan extensions, and fine collection.
