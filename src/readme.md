# Source Code

This folder contains the main source code for the Liana's Library Management System.

## Files

- **`app.py`** — Main Streamlit application that provides the user interface, navigation, and dashboard.
- **`create.py`** — Handles creation of books, users, and loans.
- **`read.py`** — Displays book, user, and active loan information.
- **`update.py`** — Handles updates to books, users, and loans, including loan extensions, returns, and fine management.
- **`delete.py`** — Handles deletion of books and users.
- **`.streamlit/secrets.toml`** — Stores sensitive database configuration and credentials. This file should not be committed to GitHub.

## Application Structure

The application uses a modular CRUD structure:

```text
app.py
  │
  ├── create.py
  ├── read.py
  ├── update.py
  └── delete.py
