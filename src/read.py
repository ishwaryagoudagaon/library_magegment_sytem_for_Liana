import pandas as pd
from datetime import date, timedelta, datetime
from sqlalchemy import text
import db
import streamlit as st
engine = db.get_engine()


def read_user_page(engine):
    st.subheader("User Details")

    try:
        query = text("""
            SELECT
                user_id,
                user_name,
                phone_number,
                email,
                max_loans
            FROM users
            ORDER BY user_id
        """)

        with engine.connect() as connection:
            result = connection.execute(query)

            users = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )

        if users.empty:
            st.info("No users found.")

        else:
            st.dataframe(
                users,
                use_container_width=True,
                hide_index=True
            )

    except Exception as error:
        st.error(f"Error reading users: {error}")

def read_loan_page(engine):

    st.subheader("Loan Details")

    try:
        with engine.connect() as connection:

            result = connection.execute(
                text("""
                    SELECT
                        l.loan_id,
                        l.isbn,
                        b.title AS book_title,
                        l.user_id,
                        u.user_name,
                        u.max_loans,
                        l.loan_date,
                        l.due_date,
                        l.extended_due_date,
                        l.extension_count,
                        l.late_fee,
                        l.return_date,
                        l.fine_paid_date
                    FROM loans l
                    INNER JOIN books b
                        ON l.isbn = b.isbn
                    INNER JOIN users u
                        ON l.user_id = u.user_id
                    WHERE l.return_date IS NULL
                    ORDER BY l.loan_id
                """)
            )

            loans = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )

        if loans.empty:

            st.info("No active loans found.")

        else:

            st.dataframe(
                loans,
                use_container_width=True,
                hide_index=True
            )

    except Exception as error:

        st.error(f"Error reading loans: {error}")
    

def read_book_page(engine):
    st.subheader("Book Details")

    try:
        query = text("""
            SELECT
                b.isbn,
                b.title,
                b.author,
                b.genre,
                b.book_language,

                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM loans l
                        WHERE l.isbn = b.isbn
                          AND l.return_date IS NULL
                    )
                    THEN 'Not Available'
                    ELSE 'Available'
                END AS is_available

            FROM books b
            ORDER BY b.isbn
        """)

        with engine.connect() as connection:
            result = connection.execute(query)

            books = pd.DataFrame(
                result.fetchall(),
                columns=result.keys()
            )

        if books.empty:
            st.info("No books found.")

        else:
            # Add numbering starting from 1
            books.insert(
                0,
                "No.",
                range(1, len(books) + 1)
            )

            # Display table
            st.dataframe(
                books,
                use_container_width=True,
                hide_index=True
            )

    except Exception as error:
        st.error(f"Error reading books: {error}")