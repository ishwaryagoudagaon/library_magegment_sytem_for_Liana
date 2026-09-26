import pandas as pd
from datetime import date, timedelta, datetime
from sqlalchemy import text
import db
import streamlit as st

engine = db.get_engine()

def modify_user_page(engine):
    st.subheader("Modify User")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    if st.button("Find User"):

        with engine.connect() as connection:
            user = connection.execute(
                text("""
                    SELECT
                        user_id,
                        user_name,
                        phone_number,
                        email,
                        max_loans
                    FROM users
                    WHERE user_id = :user_id
                """),
                {"user_id": user_id}
            ).mappings().fetchone()

        if not user:
            st.error("User not found.")
            return

        st.session_state["user_to_modify"] = dict(user)

    if "user_to_modify" not in st.session_state:
        return

    user = st.session_state["user_to_modify"]

    st.success(f"User found: {user['user_name']}")

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "User Name",
            "Phone Number",
            "Email",
            "Maximum Loans"
        ]
    )

    if field_to_modify == "User Name":
        new_value = st.text_input(
            "New User Name",
            value=user["user_name"]
        )
        database_column = "user_name"

    elif field_to_modify == "Phone Number":
        new_value = st.text_input(
            "New Phone Number",
            value=user["phone_number"]
        )
        database_column = "phone_number"

    elif field_to_modify == "Email":
        new_value = st.text_input(
            "New Email",
            value=user["email"]
        )
        database_column = "email"

    else:
        new_value = st.number_input(
            "New Maximum Loans",
            min_value=1,
            value=int(user["max_loans"]),
            step=1
        )
        database_column = "max_loans"

    if st.button("Update User"):

        if isinstance(new_value, str):
            new_value = new_value.strip()

            if not new_value:
                st.error("The new value cannot be empty.")
                return

        try:
            with engine.begin() as connection:
                connection.execute(
                    text(f"""
                        UPDATE users
                        SET {database_column} = :new_value
                        WHERE user_id = :user_id
                    """),
                    {
                        "new_value": new_value,
                        "user_id": user["user_id"]
                    }
                )

            st.success("User updated successfully.")

            del st.session_state["user_to_modify"]

        except Exception as error:
            st.error(f"Error updating user: {error}")


def modify_book_page(engine):
    st.subheader("Modify Book")

    isbn = st.text_input("Enter ISBN")

    if st.button("Find Book"):
        isbn = isbn.strip().replace("-", "").replace(" ", "")

        if not isbn:
            st.error("Please enter an ISBN.")
            return

        with engine.connect() as connection:
            book = connection.execute(
                text("""
                    SELECT isbn, title, author, genre,
                           book_language, is_available
                    FROM books
                    WHERE isbn = :isbn
                """),
                {"isbn": isbn}
            ).mappings().fetchone()

        if not book:
            st.error("Book not found.")
            return

        st.session_state["book_to_modify"] = dict(book)

    if "book_to_modify" not in st.session_state:
        return

    book = st.session_state["book_to_modify"]

    st.success(f"Book found: {book['title']}")

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "Title",
            "Author",
            "Genre",
            "Book Language",
            "Is Available"
        ]
    )

    if field_to_modify == "Title":
        new_value = st.text_input(
            "New Title",
            value=book["title"]
        )
        database_column = "title"

    elif field_to_modify == "Author":
        new_value = st.text_input(
            "New Author",
            value=book["author"]
        )
        database_column = "author"

    elif field_to_modify == "Genre":
        new_value = st.text_input(
            "New Genre",
            value=book["genre"]
        )
        database_column = "genre"

    elif field_to_modify == "Book Language":
        new_value = st.text_input(
            "New Book Language",
            value=book["book_language"]
        )
        database_column = "book_language"

    else:
        current_status = bool(book["is_available"])

        new_value = st.selectbox(
            "Availability",
            ["Available", "Not Available"],
            index=0 if current_status else 1
        )

        new_value = new_value == "Available"
        database_column = "is_available"

    if st.button("Update Book"):
        if isinstance(new_value, str):
            new_value = new_value.strip()

            if not new_value:
                st.error("The new value cannot be empty.")
                return

        try:
            with engine.begin() as connection:
                connection.execute(
                    text(f"""
                        UPDATE books
                        SET {database_column} = :new_value
                        WHERE isbn = :isbn
                    """),
                    {
                        "new_value": new_value,
                        "isbn": book["isbn"]
                    }
                )

            st.success("Book updated successfully.")

            # Remove old data so the user can search again
            del st.session_state["book_to_modify"]

        except Exception as error:
            st.error(f"Error updating book: {error}")


# ============================================================
# USER UPDATE
# ============================================================

def modify_user_page(engine):
    st.subheader("Modify User")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    if st.button("Find User"):
        try:
            with engine.connect() as connection:
                user = connection.execute(
                    text("""
                        SELECT
                            user_id,
                            user_name,
                            phone_number,
                            email,
                            max_loans
                        FROM users
                        WHERE user_id = :user_id
                    """),
                    {"user_id": user_id}
                ).mappings().fetchone()

            if not user:
                st.error("User not found.")
                return

            st.session_state["user_to_modify"] = dict(user)

        except Exception as error:
            st.error(f"Error finding user: {error}")

    if "user_to_modify" not in st.session_state:
        return

    user = st.session_state["user_to_modify"]

    st.success(
        f"User found: {user['user_name']} "
        f"(ID: {user['user_id']})"
    )

    st.write(f"**Current Phone:** {user['phone_number']}")
    st.write(f"**Current Email:** {user['email']}")
    st.write(f"**Current Available Loans:** {user['max_loans']}")

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "User Name",
            "Phone Number",
            "Email",
            "Maximum Loans"
        ]
    )

    if field_to_modify == "User Name":

        new_value = st.text_input(
            "New User Name",
            value=user["user_name"]
        )

        database_column = "user_name"

    elif field_to_modify == "Phone Number":

        new_value = st.text_input(
            "New Phone Number",
            value=user["phone_number"]
        )

        database_column = "phone_number"

    elif field_to_modify == "Email":

        new_value = st.text_input(
            "New Email",
            value=user["email"]
        )

        database_column = "email"

    else:

        new_value = st.number_input(
            "New Maximum Loans",
            min_value=0,
            value=int(user["max_loans"]),
            step=1
        )

        database_column = "max_loans"

    if st.button("Update User"):

        if isinstance(new_value, str):
            new_value = new_value.strip()

            if not new_value:
                st.error("The new value cannot be empty.")
                return

        try:

            with engine.begin() as connection:

                connection.execute(
                    text(f"""
                        UPDATE users
                        SET {database_column} = :new_value
                        WHERE user_id = :user_id
                    """),
                    {
                        "new_value": new_value,
                        "user_id": user["user_id"]
                    }
                )

            st.success("User updated successfully.")

            del st.session_state["user_to_modify"]

        except Exception as error:

            st.error(f"Error updating user: {error}")


# ============================================================
# BOOK UPDATE
# ============================================================

def modify_book_page(engine):
    st.subheader("Modify Book")

    isbn = st.text_input("Enter ISBN")

    if st.button("Find Book"):

        isbn = (
            isbn
            .strip()
            .replace("-", "")
            .replace(" ", "")
        )

        if not isbn:
            st.error("Please enter an ISBN.")
            return

        try:

            with engine.connect() as connection:

                book = connection.execute(
                    text("""
                        SELECT
                            isbn,
                            title,
                            author,
                            genre,
                            book_language,
                            is_available
                        FROM books
                        WHERE isbn = :isbn
                    """),
                    {"isbn": isbn}
                ).mappings().fetchone()

            if not book:
                st.error("Book not found.")
                return

            st.session_state["book_to_modify"] = dict(book)

        except Exception as error:

            st.error(f"Error finding book: {error}")

    if "book_to_modify" not in st.session_state:
        return

    book = st.session_state["book_to_modify"]

    st.success(
        f"Book found: {book['title']} "
        f"(ISBN: {book['isbn']})"
    )

    current_status = bool(book["is_available"])

    st.write(
        "**Current Availability:** "
        + (
            "Available for Loan"
            if current_status
            else "Currently Loaned"
        )
    )

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "Title",
            "Author",
            "Genre",
            "Book Language",
            "Is Available"
        ]
    )

    if field_to_modify == "Title":

        new_value = st.text_input(
            "New Title",
            value=book["title"]
        )

        database_column = "title"

    elif field_to_modify == "Author":

        new_value = st.text_input(
            "New Author",
            value=book["author"] or ""
        )

        database_column = "author"

    elif field_to_modify == "Genre":

        new_value = st.text_input(
            "New Genre",
            value=book["genre"] or ""
        )

        database_column = "genre"

    elif field_to_modify == "Book Language":

        new_value = st.text_input(
            "New Book Language",
            value=book["book_language"] or ""
        )

        database_column = "book_language"

    else:

        new_value = st.selectbox(
            "Availability",
            [
                "Available",
                "Not Available"
            ],
            index=0 if current_status else 1
        )

        new_value = new_value == "Available"

        database_column = "is_available"

    if st.button("Update Book"):

        if isinstance(new_value, str):

            new_value = new_value.strip()

            if not new_value:
                st.error("The new value cannot be empty.")
                return

        try:

            with engine.begin() as connection:

                connection.execute(
                    text(f"""
                        UPDATE books
                        SET {database_column} = :new_value
                        WHERE isbn = :isbn
                    """),
                    {
                        "new_value": new_value,
                        "isbn": book["isbn"]
                    }
                )

            st.success("Book updated successfully.")

            del st.session_state["book_to_modify"]

        except Exception as error:

            st.error(f"Error updating book: {error}")


# ============================================================
# LOAN UPDATE
# ============================================================


FINE_PER_DAY = 0.25

MAX_EXTENSIONS = 2

EXTENSION_DAYS = 10


# ============================================================
# USER UPDATE
# ============================================================

def modify_user_page(engine):

    st.subheader("Modify User")

    user_id = st.number_input(
        "Enter User ID",
        min_value=1,
        step=1
    )

    if st.button("Find User"):

        try:

            with engine.connect() as connection:

                user = connection.execute(
                    text("""
                        SELECT
                            user_id,
                            user_name,
                            phone_number,
                            email,
                            max_loans
                        FROM users
                        WHERE user_id = :user_id
                    """),
                    {
                        "user_id": user_id
                    }
                ).mappings().fetchone()

            if not user:

                st.error("User not found.")
                return

            st.session_state["user_to_modify"] = dict(user)

        except Exception as error:

            st.error(
                f"Error finding user: {error}"
            )

    if "user_to_modify" not in st.session_state:
        return

    user = st.session_state["user_to_modify"]

    st.success(
        f"User found: {user['user_name']} "
        f"(ID: {user['user_id']})"
    )

    st.write(
        f"**Current User Name:** "
        f"{user['user_name']}"
    )

    st.write(
        f"**Current Phone Number:** "
        f"{user['phone_number']}"
    )

    st.write(
        f"**Current Email:** "
        f"{user['email']}"
    )

    st.write(
        f"**Available Loan Allowance:** "
        f"{user['max_loans']}"
    )

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "User Name",
            "Phone Number",
            "Email"
        ]
    )

    if field_to_modify == "User Name":

        new_value = st.text_input(
            "New User Name",
            value=user["user_name"]
        )

        database_column = "user_name"

    elif field_to_modify == "Phone Number":

        new_value = st.text_input(
            "New Phone Number",
            value=user["phone_number"]
        )

        database_column = "phone_number"

    else:

        new_value = st.text_input(
            "New Email",
            value=user["email"]
        )

        database_column = "email"

    if st.button("Update User"):

        new_value = new_value.strip()

        if not new_value:

            st.error(
                "The new value cannot be empty."
            )

            return

        try:

            with engine.begin() as connection:

                if database_column == "email":

                    existing_user = connection.execute(
                        text("""
                            SELECT user_id
                            FROM users
                            WHERE email = :email
                              AND user_id != :user_id
                        """),
                        {
                            "email": new_value,
                            "user_id": user["user_id"]
                        }
                    ).first()

                    if existing_user:

                        st.error(
                            "This email is already used "
                            "by another user."
                        )

                        return

                if database_column == "phone_number":

                    existing_user = connection.execute(
                        text("""
                            SELECT user_id
                            FROM users
                            WHERE phone_number = :phone_number
                              AND user_id != :user_id
                        """),
                        {
                            "phone_number": new_value,
                            "user_id": user["user_id"]
                        }
                    ).first()

                    if existing_user:

                        st.error(
                            "This phone number is already "
                            "used by another user."
                        )

                        return

                connection.execute(
                    text(f"""
                        UPDATE users
                        SET {database_column} = :new_value
                        WHERE user_id = :user_id
                    """),
                    {
                        "new_value": new_value,
                        "user_id": user["user_id"]
                    }
                )

            st.success(
                "User updated successfully."
            )

            del st.session_state[
                "user_to_modify"
            ]

        except Exception as error:

            st.error(
                f"Error updating user: {error}"
            )


# ============================================================
# BOOK UPDATE
# ============================================================

def modify_book_page(engine):

    st.subheader("Modify Book")

    isbn = st.text_input(
        "Enter ISBN"
    )

    if st.button("Find Book"):

        isbn = (
            isbn
            .strip()
            .replace("-", "")
            .replace(" ", "")
        )

        if not isbn:

            st.error(
                "Please enter an ISBN."
            )

            return

        try:

            with engine.connect() as connection:

                book = connection.execute(
                    text("""
                        SELECT
                            isbn,
                            title,
                            author,
                            genre,
                            book_language,
                            is_available
                        FROM books
                        WHERE isbn = :isbn
                    """),
                    {
                        "isbn": isbn
                    }
                ).mappings().fetchone()

            if not book:

                st.error(
                    "Book not found."
                )

                return

            st.session_state[
                "book_to_modify"
            ] = dict(book)

        except Exception as error:

            st.error(
                f"Error finding book: {error}"
            )

    if "book_to_modify" not in st.session_state:
        return

    book = st.session_state[
        "book_to_modify"
    ]

    st.success(
        f"Book found: {book['title']} "
        f"(ISBN: {book['isbn']})"
    )

    current_status = bool(
        book["is_available"]
    )

    st.write(
        "**Current Availability:** "
        +
        (
            "Available for Loan"
            if current_status
            else "Currently Loaned"
        )
    )

    field_to_modify = st.selectbox(
        "What do you want to modify?",
        [
            "Title",
            "Author",
            "Genre",
            "Book Language",
            "Is Available"
        ]
    )

    if field_to_modify == "Title":

        new_value = st.text_input(
            "New Title",
            value=book["title"]
        )

        database_column = "title"

    elif field_to_modify == "Author":

        new_value = st.text_input(
            "New Author",
            value=book["author"] or ""
        )

        database_column = "author"

    elif field_to_modify == "Genre":

        new_value = st.text_input(
            "New Genre",
            value=book["genre"] or ""
        )

        database_column = "genre"

    elif field_to_modify == "Book Language":

        new_value = st.text_input(
            "New Book Language",
            value=book["book_language"] or ""
        )

        database_column = "book_language"

    else:

        new_value = st.selectbox(
            "Availability",
            [
                "Available",
                "Not Available"
            ],
            index=0 if current_status else 1
        )

        new_value = (
            new_value == "Available"
        )

        database_column = "is_available"

    if st.button("Update Book"):

        if isinstance(new_value, str):

            new_value = new_value.strip()

            if not new_value:

                st.error(
                    "The new value cannot be empty."
                )

                return

        try:

            with engine.begin() as connection:

                connection.execute(
                    text(f"""
                        UPDATE books
                        SET {database_column} = :new_value
                        WHERE isbn = :isbn
                    """),
                    {
                        "new_value": new_value,
                        "isbn": book["isbn"]
                    }
                )

            st.success(
                "Book updated successfully."
            )

            del st.session_state[
                "book_to_modify"
            ]

        except Exception as error:

            st.error(
                f"Error updating book: {error}"
            )


# ============================================================
# LOAN UPDATE
# ============================================================

def modify_loan_page(engine):

    st.subheader("Modify Loan")

    # ========================================================
    # FIND LOAN
    # ========================================================

    loan_id = st.number_input(
        "Enter Loan ID",
        min_value=1,
        step=1
    )

    if st.button("Find Loan"):

        try:

            with engine.connect() as connection:

                loan = connection.execute(
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

                        WHERE l.loan_id = :loan_id
                    """),
                    {
                        "loan_id": loan_id
                    }
                ).mappings().fetchone()

            if not loan:

                st.error(
                    "Loan not found."
                )

                return

            st.session_state[
                "loan_to_modify"
            ] = dict(loan)

        except Exception as error:

            st.error(
                f"Error finding loan: {error}"
            )

    if "loan_to_modify" not in st.session_state:
        return

    loan = st.session_state[
        "loan_to_modify"
    ]

    # ========================================================
    # DISPLAY LOAN INFORMATION
    # ========================================================

    st.success(
        f"Loan found: #{loan['loan_id']}"
    )

    st.write(
        f"**Book:** {loan['book_title']}"
    )

    st.write(
        f"**ISBN:** {loan['isbn']}"
    )

    st.write(
        f"**User:** {loan['user_name']} "
        f"(ID: {loan['user_id']})"
    )

    st.write(
        f"**Loan Date:** {loan['loan_date']}"
    )

    # --------------------------------------------------------
    # Due Date cannot be changed
    # --------------------------------------------------------

    st.write(
        f"**Due Date:** {loan['due_date']}"
    )

    # --------------------------------------------------------
    # Extended Due Date
    # --------------------------------------------------------

    if loan["extended_due_date"] is not None:

        st.write(
            f"**Extended Due Date:** "
            f"{loan['extended_due_date']}"
        )

    else:

        st.write(
            "**Extended Due Date:** None"
        )

    # --------------------------------------------------------
    # Extension count
    # --------------------------------------------------------

    extension_count = int(
        loan["extension_count"]
    )

    extensions_remaining = max(
        0,
        MAX_EXTENSIONS - extension_count
    )

    st.write(
        f"**Extensions Used:** "
        f"{extension_count}/{MAX_EXTENSIONS}"
    )

    st.write(
        f"**Extensions Remaining:** "
        f"{extensions_remaining}"
    )

    # --------------------------------------------------------
    # Late Fee
    # --------------------------------------------------------

    # The automatic current fine is displayed after
    # the fine calculation below.

    # --------------------------------------------------------
    # Return Date
    # --------------------------------------------------------

    if loan["return_date"] is not None:

        st.write(
            f"**Return Date:** "
            f"{loan['return_date']}"
        )

    else:

        st.write(
            "**Return Date:** Not Returned"
        )

    # --------------------------------------------------------
    # Fine Paid Date
    # --------------------------------------------------------

    if loan["fine_paid_date"] is not None:

        st.write(
            f"**Fine Paid Date:** "
            f"{loan['fine_paid_date']}"
        )

    else:

        st.write(
            "**Fine Paid Date:** Not Paid"
        )

    # ========================================================
    # EFFECTIVE DUE DATE
    # ========================================================

    if loan["extended_due_date"] is not None:

        effective_due_date = (
            loan["extended_due_date"]
        )

    else:

        effective_due_date = (
            loan["due_date"]
        )

    # ========================================================
    # AUTOMATIC FINE CALCULATION
    # ========================================================

    if loan["return_date"] is not None:

        fine_calculation_date = (
            loan["return_date"]
        )

    else:

        fine_calculation_date = date.today()

    overdue_days = max(
        0,
        (
            fine_calculation_date
            - effective_due_date
        ).days
    )

    current_fine = round(
        overdue_days * FINE_PER_DAY,
        2
    )

    # --------------------------------------------------------
    # Automatically save the calculated late fee to MySQL.
    #
    # The user cannot manually change this value.
    # --------------------------------------------------------

    try:

        if loan["return_date"] is None:

            with engine.begin() as connection:

                connection.execute(
                    text("""
                        UPDATE loans
                        SET late_fee = :late_fee
                        WHERE loan_id = :loan_id
                          AND return_date IS NULL
                    """),
                    {
                        "late_fee": current_fine,
                        "loan_id": loan["loan_id"]
                    }
                )

    except Exception as error:

        st.error(
            f"Error updating automatic late fee: {error}"
        )

    # --------------------------------------------------------
    # Show automatic fine information
    # --------------------------------------------------------

    st.write(
        f"**Current Late Fee:** ${current_fine:.2f}"
    )

    if overdue_days > 0:

        st.warning(
            f"This loan is {overdue_days} day(s) overdue."
        )

        st.warning(
            f"Current fine: ${current_fine:.2f}"
        )

    else:

        st.info(
            "This loan is not currently overdue."
        )

    # ========================================================
    # ACTIONS
    #
    # Extension Count and Late Fee are automatic.
    # They cannot be manually changed.
    # ========================================================

    action = st.selectbox(
        "What do you want to modify?",
        [
            "Update Extended Due Date",
            "Update Return Date",
            "Update Fine Paid Date"
        ]
    )

    # ========================================================
    # 1. UPDATE EXTENDED DUE DATE
    # ========================================================

    if action == "Update Extended Due Date":

        # ----------------------------------------------------
        # Already returned
        # ----------------------------------------------------

        if loan["return_date"] is not None:

            st.warning(
                "This book has already been returned. "
                "The extended due date cannot be changed."
            )

            return

        # ----------------------------------------------------
        # Maximum extension check
        # ----------------------------------------------------

        if extension_count >= MAX_EXTENSIONS:

            st.error(
                "The maximum of 2 extensions has already "
                "been used."
            )

            st.warning(
                "No further extension is allowed. "
                "Please return the book."
            )

            return

        # ----------------------------------------------------
        # Cannot extend after becoming overdue
        # ----------------------------------------------------

        if date.today() > effective_due_date:

            st.error(
                "This loan is already overdue."
            )

            st.warning(
                "The book cannot be extended after the "
                "due date has passed. Please return the "
                "book and pay the fine."
            )

            return

        # ----------------------------------------------------
        # AUTOMATIC 10-DAY EXTENSION
        #
        # No date input is provided.
        #
        # First extension:
        # original due date + 10 days
        #
        # Second extension:
        # first extended date + 10 days
        # ----------------------------------------------------

        new_extended_due_date = (
            effective_due_date
            + timedelta(days=EXTENSION_DAYS)
        )

        new_extension_count = (
            extension_count + 1
        )

        # ----------------------------------------------------
        # Display exactly what will happen
        # ----------------------------------------------------

        st.write(
            f"**Current Effective Due Date:** "
            f"{effective_due_date}"
        )

        st.write(
            f"**Extensions Used:** "
            f"{extension_count}/{MAX_EXTENSIONS}"
        )

        st.write(
            f"**Extensions Remaining:** "
            f"{MAX_EXTENSIONS - extension_count}"
        )

        st.info(
            f"An extension automatically adds "
            f"exactly {EXTENSION_DAYS} days."
        )

        st.write(
            f"**New Extended Due Date:** "
            f"{new_extended_due_date}"
        )

        st.write(
            f"**New Extension Count:** "
            f"{new_extension_count}/{MAX_EXTENSIONS}"
        )

        # ----------------------------------------------------
        # Confirm extension
        # ----------------------------------------------------

        if st.button(
            "Extend Book by 10 Days"
        ):

            try:

                with engine.begin() as connection:

                    # ----------------------------------------
                    # Re-check the database value before
                    # updating. This prevents a third
                    # extension if the database already
                    # contains 2 extensions.
                    # ----------------------------------------

                    current_loan = connection.execute(
                        text("""
                            SELECT
                                extended_due_date,
                                due_date,
                                extension_count,
                                return_date
                            FROM loans
                            WHERE loan_id = :loan_id
                            FOR UPDATE
                        """),
                        {
                            "loan_id":
                                loan["loan_id"]
                        }
                    ).mappings().fetchone()

                    if current_loan is None:

                        st.error(
                            "Loan no longer exists."
                        )

                        return

                    current_count = int(
                        current_loan["extension_count"]
                    )

                    if current_loan["return_date"] is not None:

                        st.error(
                            "This book has already been returned."
                        )

                        return

                    if current_count >= MAX_EXTENSIONS:

                        st.error(
                            "The maximum of 2 extensions "
                            "has already been used."
                        )

                        st.warning(
                            "Please return the book."
                        )

                        return

                    # ----------------------------------------
                    # Get the current effective due date
                    # directly from the database.
                    # ----------------------------------------

                    if (
                        current_loan["extended_due_date"]
                        is not None
                    ):

                        database_effective_due_date = (
                            current_loan[
                                "extended_due_date"
                            ]
                        )

                    else:

                        database_effective_due_date = (
                            current_loan[
                                "due_date"
                            ]
                        )

                    # ----------------------------------------
                    # Do not allow extension after due date
                    # ----------------------------------------

                    if (
                        date.today()
                        > database_effective_due_date
                    ):

                        st.error(
                            "This loan is already overdue. "
                            "The book cannot be extended."
                        )

                        st.warning(
                            "Please return the book "
                            "and pay the fine."
                        )

                        return

                    # ----------------------------------------
                    # Calculate exactly 10 days
                    # ----------------------------------------

                    database_new_date = (
                        database_effective_due_date
                        + timedelta(
                            days=EXTENSION_DAYS
                        )
                    )

                    database_new_count = (
                        current_count + 1
                    )

                    # ----------------------------------------
                    # Update BOTH values together
                    # ----------------------------------------

                    result = connection.execute(
                        text("""
                            UPDATE loans
                            SET
                                extended_due_date =
                                    :extended_due_date,

                                extension_count =
                                    :extension_count

                            WHERE loan_id = :loan_id
                              AND extension_count < 2
                              AND return_date IS NULL
                        """),
                        {
                            "extended_due_date":
                                database_new_date,

                            "extension_count":
                                database_new_count,

                            "loan_id":
                                loan["loan_id"]
                        }
                    )

                    if result.rowcount != 1:

                        st.error(
                            "The extension could not be completed. "
                            "The maximum of 2 extensions may already "
                            "have been reached."
                        )

                        return

                # ------------------------------------------------
                # Success
                # ------------------------------------------------

                st.success(
                    "Book extended successfully."
                )

                st.success(
                    f"New Extended Due Date: "
                    f"{database_new_date}"
                )

                st.success(
                    f"Extensions Used: "
                    f"{database_new_count}/2"
                )

                if database_new_count == MAX_EXTENSIONS:

                    st.warning(
                        "Both extensions have now been used. "
                        "No further extension is allowed. "
                        "Please return the book."
                    )

                else:

                    st.info(
                        "One extension remains."
                    )

                # Clear old session data
                del st.session_state[
                    "loan_to_modify"
                ]

                # Reload the page
                st.rerun()

            except Exception as error:

                st.error(
                    f"Error extending book: {error}"
                )

    # ========================================================
    # 2. UPDATE RETURN DATE
    # ========================================================

    elif action == "Update Return Date":

        # ----------------------------------------------------
        # Return can only happen once
        # ----------------------------------------------------

        if loan["return_date"] is not None:

            st.warning(
                f"This book was already returned on "
                f"{loan['return_date']}."
            )

            st.info(
                "The return date can only be recorded once."
            )

            return

        return_date = st.date_input(
            "Return Date",
            value=date.today()
        )

        if return_date < loan["loan_date"]:

            st.error(
                "Return date cannot be before "
                "the loan date."
            )

            return

        # ----------------------------------------------------
        # Calculate final fine using the FINAL
        # effective due date.
        # ----------------------------------------------------

        return_overdue_days = max(
            0,
            (
                return_date
                - effective_due_date
            ).days
        )

        final_fine = round(
            return_overdue_days
            * FINE_PER_DAY,
            2
        )

        st.write(
            f"**Effective Due Date:** "
            f"{effective_due_date}"
        )

        st.write(
            f"**Return Date:** "
            f"{return_date}"
        )

        st.write(
            f"**Overdue Days:** "
            f"{return_overdue_days}"
        )

        st.write(
            f"**Final Fine:** "
            f"${final_fine:.2f}"
        )

        # ----------------------------------------------------
        # Fine payment
        # ----------------------------------------------------

        if final_fine > 0:

            st.warning(
                f"Fine due: ${final_fine:.2f}"
            )

            st.info(
                "The fine must be paid when "
                "the book is returned."
            )

            fine_paid = st.checkbox(
                "I confirm that the fine has been paid."
            )

            if not fine_paid:

                st.error(
                    "Please confirm that the fine "
                    "has been paid."
                )

                return

            # Fine payment happens on the return date
            fine_paid_date = return_date

        else:

            st.success(
                "No fine is due for this return."
            )

            fine_paid_date = None

        # ----------------------------------------------------
        # Confirm book returned
        # ----------------------------------------------------

        confirm_return = st.checkbox(
            "I confirm that the book has been returned."
        )

        if not confirm_return:

            st.info(
                "Please confirm that the book "
                "has been returned."
            )

            return

        if st.button(
            "Complete Book Return"
        ):

            try:

                with engine.begin() as connection:

                    # ----------------------------------------
                    # Update loan
                    # ----------------------------------------

                    connection.execute(
                        text("""
                            UPDATE loans
                            SET
                                return_date =
                                    :return_date,

                                late_fee =
                                    :late_fee,

                                fine_paid_date =
                                    :fine_paid_date

                            WHERE loan_id =
                                :loan_id

                              AND return_date IS NULL
                        """),
                        {
                            "return_date":
                                return_date,

                            "late_fee":
                                final_fine,

                            "fine_paid_date":
                                fine_paid_date,

                            "loan_id":
                                loan["loan_id"]
                        }
                    )

                    # ----------------------------------------
                    # Make book available
                    # ----------------------------------------

                    connection.execute(
                        text("""
                            UPDATE books
                            SET is_available = TRUE
                            WHERE isbn = :isbn
                        """),
                        {
                            "isbn":
                                loan["isbn"]
                        }
                    )

                    # ----------------------------------------
                    # Restore user's loan allowance
                    # ----------------------------------------

                    connection.execute(
                        text("""
                            UPDATE users
                            SET max_loans =
                                max_loans + 1
                            WHERE user_id = :user_id
                        """),
                        {
                            "user_id":
                                loan["user_id"]
                        }
                    )

                # ------------------------------------------------
                # Success messages
                # ------------------------------------------------

                if final_fine > 0:

                    st.success(
                        f"Book returned successfully."
                    )

                    st.success(
                        f"Fine of ${final_fine:.2f} "
                        f"was paid on {fine_paid_date}."
                    )

                else:

                    st.success(
                        "Book returned successfully."
                    )

                    st.success(
                        "No fine was due."
                    )

                st.success(
                    "The book is now available "
                    "for the next user."
                )

                st.success(
                    "The user's available loan "
                    "allowance has increased by 1."
                )

                del st.session_state[
                    "loan_to_modify"
                ]

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error returning book: "
                    f"{error}"
                )

    # ========================================================
    # 3. UPDATE FINE PAID DATE
    # ========================================================

    elif action == "Update Fine Paid Date":

        # ----------------------------------------------------
        # Book must be returned first
        # ----------------------------------------------------

        if loan["return_date"] is None:

            st.warning(
                "The book must be returned before "
                "a fine payment date can be recorded."
            )

            return

        # ----------------------------------------------------
        # Fine paid date can only be recorded once
        # ----------------------------------------------------

        if loan["fine_paid_date"] is not None:

            st.warning(
                f"The fine was already paid on "
                f"{loan['fine_paid_date']}."
            )

            st.info(
                "The fine-paid date can only be "
                "recorded once."
            )

            return

        new_fine_paid_date = st.date_input(
            "Fine Paid Date",
            value=date.today()
        )

        if new_fine_paid_date < loan["loan_date"]:

            st.error(
                "Fine paid date cannot be before "
                "the loan date."
            )

            return

        if new_fine_paid_date < loan["return_date"]:

            st.error(
                "Fine paid date cannot be before "
                "the return date."
            )

            return

        if st.button(
            "Update Fine Paid Date"
        ):

            try:

                with engine.begin() as connection:

                    connection.execute(
                        text("""
                            UPDATE loans
                            SET fine_paid_date =
                                :fine_paid_date
                            WHERE loan_id =
                                :loan_id
                        """),
                        {
                            "fine_paid_date":
                                new_fine_paid_date,

                            "loan_id":
                                loan["loan_id"]
                        }
                    )

                st.success(
                    "Fine paid date updated successfully."
                )

                del st.session_state[
                    "loan_to_modify"
                ]

                st.rerun()

            except Exception as error:

                st.error(
                    f"Error updating fine paid date: "
                    f"{error}"
                )
