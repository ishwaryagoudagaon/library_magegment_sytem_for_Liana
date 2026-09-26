import pandas as pd
from datetime import date, timedelta, datetime
from sqlalchemy import text
import db
import streamlit as st

engine = db.get_engine()

#-----------------------------
# Delete users

def delete_user_page(engine):
    st.subheader("Delete User")

    user_id = st.number_input(
        "Enter User ID of the user to delete",
        min_value=1,
        step=1
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this user"
    )

    if st.button("Delete User"):

        if not confirm_delete:
            st.warning("Please confirm deletion first.")
            return

        try:
            with engine.begin() as connection:

                user_exists = connection.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1
                            FROM users
                            WHERE user_id = :user_id
                        )
                    """),
                    {"user_id": user_id}
                ).scalar()

                if not user_exists:
                    st.error(
                        f"User with ID {user_id} does not exist."
                    )
                    return

                loan_exists = connection.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1
                            FROM loans
                            WHERE user_id = :user_id
                        )
                    """),
                    {"user_id": user_id}
                ).scalar()

                if loan_exists:
                    st.warning(
                        f"User with ID {user_id} cannot be deleted "
                        "because loan records exist."
                    )
                    return

                result = connection.execute(
                    text("""
                        DELETE FROM users
                        WHERE user_id = :user_id
                    """),
                    {"user_id": user_id}
                )

                if result.rowcount == 1:
                    st.success(
                        f"User with ID {user_id} deleted successfully."
                    )
                else:
                    st.error(
                        f"User with ID {user_id} was not deleted."
                    )

        except Exception as error:
            st.error(f"Database error: {error}")



def delete_book_page(engine):
    st.subheader("Delete Book")

    isbn = st.text_input("Enter ISBN of the book to delete")

    confirm_delete = st.checkbox(
        "I confirm that I want to delete this book"
    )

    if st.button("Delete Book"):

        isbn = isbn.strip().replace("-", "").replace(" ", "")

        if not isbn:
            st.error("Please enter an ISBN.")
            return

        if not confirm_delete:
            st.warning("Please confirm deletion first.")
            return

        try:
            with engine.begin() as connection:

                book_exists = connection.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1
                            FROM books
                            WHERE isbn = :isbn
                        )
                    """),
                    {"isbn": isbn}
                ).scalar()

                if not book_exists:
                    st.error(
                        f"Book with ISBN {isbn} does not exist."
                    )
                    return

                loan_exists = connection.execute(
                    text("""
                        SELECT EXISTS (
                            SELECT 1
                            FROM loans
                            WHERE isbn = :isbn
                        )
                    """),
                    {"isbn": isbn}
                ).scalar()

                if loan_exists:
                    st.warning(
                        f"Book with ISBN {isbn} cannot be deleted "
                        "because loan records exist."
                    )
                    return

                result = connection.execute(
                    text("""
                        DELETE FROM books
                        WHERE isbn = :isbn
                    """),
                    {"isbn": isbn}
                )

                if result.rowcount == 1:
                    st.success(
                        f"Book with ISBN {isbn} deleted successfully."
                    )
                else:
                    st.error(
                        f"Book with ISBN {isbn} was not deleted."
                    )

        except Exception as error:
            st.error(f"Database error: {error}")






