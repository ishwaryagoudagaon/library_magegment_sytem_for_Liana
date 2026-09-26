import pandas as pd
from datetime import date, timedelta, datetime
from sqlalchemy import text
import db
import streamlit as st

engine = db.get_engine()
from sqlalchemy.exc import IntegrityError
import re
from datetime import datetime


def create_book_page(engine):
    st.title("Create Book")

    with st.form("create_book_form"):
        isbn = st.text_input("ISBN")
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        book_language = st.text_input("Book Language")
        is_available = st.checkbox("Is Available", value=True)

        submitted = st.form_submit_button("Create Book")

    if submitted:
        isbn = isbn.strip().replace("-", "").replace(" ", "")
        title = title.strip()
        author = author.strip()
        genre = genre.strip()
        book_language = book_language.strip()

        if not isbn or not title or not author or not genre or not book_language:
            st.error("Please fill in all fields.")
            return

        if not re.fullmatch(r"\d{10}|\d{13}", isbn):
            st.error("ISBN must contain 10 or 13 digits.")
            return

        try:
            with engine.begin() as connection:
                existing_book = connection.execute(
                    text("""
                        SELECT isbn
                        FROM books
                        WHERE isbn = :isbn
                    """),
                    {"isbn": isbn}
                ).fetchone()

                if existing_book:
                    st.error("A book with this ISBN already exists.")
                    return

                connection.execute(
                    text("""
                        INSERT INTO books
                        (
                            isbn,
                            title,
                            author,
                            genre,
                            book_language,
                            is_available
                        )
                        VALUES
                        (
                            :isbn,
                            :title,
                            :author,
                            :genre,
                            :book_language,
                            :is_available
                        )
                    """),
                    {
                        "isbn": isbn,
                        "title": title,
                        "author": author,
                        "genre": genre,
                        "book_language": book_language,
                        "is_available": is_available
                    }
                )

            st.success("Book created successfully.")

        except IntegrityError:
            st.error("A book with this ISBN already exists.")

        except Exception as error:
            st.error(f"Error creating book: {error}")




#Create a user
def create_user_page(engine):

    st.subheader("Create User")

    # ---------------------------------------------------------
    # Input fields
    # ---------------------------------------------------------

    user_name = st.text_input(
        "User Name",
        placeholder="Enter name",
        autocomplete="off"
    )

    phone_number = st.text_input(
        "Phone Number",
        placeholder="Enter 12 digit phone number",
        autocomplete="off"
    )

    email = st.text_input(
        "Email",
        placeholder="name@gmail.com",
        autocomplete="off"
    )

    max_loans = st.number_input(
        "Maximum Loans",
        min_value=1,
        value=5,
        step=1
    )

    # ---------------------------------------------------------
    # LIVE VALIDATION
    # ---------------------------------------------------------

    name_valid = False
    phone_valid = False
    email_valid = False

    # ---------- User Name ----------

    if user_name:

        if re.fullmatch(
            r"[A-Za-z]+(?: [A-Za-z]+)*",
            user_name.strip()
        ):

            st.success("✓ User name is valid")
            name_valid = True

        else:

            st.error(
                "User name must contain letters and spaces only. "
                "Numbers and special characters are not allowed."
            )

    # ---------- Phone Number ----------

    if phone_number:

        if re.fullmatch(
            r"\d{12}",
            phone_number.strip()
        ):

            st.success("✓ Phone number is valid")
            phone_valid = True

        else:

            st.error(
                "Phone number must contain exactly 12 digits "
                "and numbers only."
            )

    # ---------- Email ----------

    if email:

        email_value = email.strip().lower()

        if re.fullmatch(
            r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|mail)\.com",
            email_value
        ):

            st.success("✓ Email is valid")
            email_valid = True

        else:

            st.error(
                "Email must be in this format: "
                "name@gmail.com, name@yahoo.com, "
                "name@outlook.com, name@hotmail.com, "
                "or name@mail.com"
            )

    # ---------------------------------------------------------
    # CREATE USER BUTTON
    # ---------------------------------------------------------

    submitted = st.button(
        "Create User",
        type="primary"
    )

    if not submitted:
        return

    # ---------------------------------------------------------
    # Check that all fields are filled
    # ---------------------------------------------------------

    user_name = " ".join(
        user_name.strip().split()
    )

    phone_number = phone_number.strip()

    email = email.strip().lower()

    if not user_name:

        st.error("Please enter the user name.")
        return

    if not phone_number:

        st.error("Please enter the phone number.")
        return

    if not email:

        st.error("Please enter the email.")
        return

    # ---------------------------------------------------------
    # Validate all fields again before database operation
    # ---------------------------------------------------------

    if not re.fullmatch(
        r"[A-Za-z]+(?: [A-Za-z]+)*",
        user_name
    ):

        st.error(
            "Invalid user name. "
            "Only letters and spaces are allowed."
        )
        return

    if not re.fullmatch(
        r"\d{12}",
        phone_number
    ):

        st.error(
            "Invalid phone number. "
            "It must contain exactly 12 digits."
        )
        return

    if not re.fullmatch(
        r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail|mail)\.com",
        email
    ):

        st.error(
            "Invalid email. Use a valid format such as "
            "name@gmail.com, name@yahoo.com, "
            "name@outlook.com, name@hotmail.com, "
            "or name@mail.com."
        )
        return

    # ---------------------------------------------------------
    # Normalization functions
    # ---------------------------------------------------------

    def normalize_name(value):

        if value is None:
            return ""

        return " ".join(
            str(value).strip().split()
        ).casefold()

    def normalize_phone(value):

        if value is None:
            return ""

        return str(value).strip()

    def normalize_email(value):

        if value is None:
            return ""

        return str(value).strip().casefold()

    # ---------------------------------------------------------
    # Normalize new user information
    # ---------------------------------------------------------

    new_name = normalize_name(user_name)
    new_phone = normalize_phone(phone_number)
    new_email = normalize_email(email)

    # ---------------------------------------------------------
    # Check database
    # ---------------------------------------------------------

    try:

        with engine.begin() as connection:

            result = connection.execute(
                text(
                    """
                    SELECT
                        user_id,
                        user_name,
                        phone_number,
                        email,
                        max_loans
                    FROM users
                    ORDER BY user_id
                    """
                )
            )

            existing_users = result.fetchall()

            # -------------------------------------------------
            # Find duplicate users
            # -------------------------------------------------

            matching_users = []

            for user in existing_users:

                existing_name = normalize_name(
                    user.user_name
                )

                existing_phone = normalize_phone(
                    user.phone_number
                )

                existing_email = normalize_email(
                    user.email
                )

                name_match = (
                    new_name == existing_name
                    and new_name != ""
                )

                phone_match = (
                    new_phone == existing_phone
                    and new_phone != ""
                )

                email_match = (
                    new_email == existing_email
                    and new_email != ""
                )

                # ANY ONE MATCH = DUPLICATE

                if (
                    name_match
                    or phone_match
                    or email_match
                ):

                    matching_users.append(
                        {
                            "user": user,
                            "name_match": name_match,
                            "phone_match": phone_match,
                            "email_match": email_match
                        }
                    )

            # -------------------------------------------------
            # DUPLICATE FOUND
            # -------------------------------------------------

            if matching_users:

                st.error(
                    "User information is already available "
                    "in the database."
                )

                st.warning(
                    "A matching user name, phone number, "
                    "or email address was found."
                )

                # ---------------------------------------------
                # Display what matched
                # ---------------------------------------------

                for match in matching_users:

                    user = match["user"]

                    if match["name_match"]:

                        st.warning(
                            f"User name already exists. "
                            f"Existing User ID: {user.user_id}"
                        )

                    if match["phone_match"]:

                        st.warning(
                            f"Phone number already exists. "
                            f"Existing User ID: {user.user_id}"
                        )

                    if match["email_match"]:

                        st.warning(
                            f"Email already exists. "
                            f"Existing User ID: {user.user_id}"
                        )

                # ---------------------------------------------
                # Display complete existing user information
                # ---------------------------------------------

                st.subheader(
                    "Existing User Details"
                )

                duplicate_data = []

                for match in matching_users:

                    user = match["user"]

                    duplicate_data.append(
                        {
                            "User ID": user.user_id,
                            "User Name": user.user_name,
                            "Phone Number": user.phone_number,
                            "Email": user.email,
                            "Maximum Loans": user.max_loans
                        }
                    )

                duplicate_df = pd.DataFrame(
                    duplicate_data
                ).drop_duplicates(
                    subset=["User ID"]
                )

                st.dataframe(
                    duplicate_df,
                    use_container_width=True,
                    hide_index=True
                )

                # ---------------------------------------------
                # Ask whether to update
                # ---------------------------------------------

                st.subheader(
                    "Would you like to update this user's information?"
                )

                update_user = st.button(
                    "Yes, Update User Information",
                    type="primary",
                    key="update_existing_user_button"
                )

                if update_user:

                    # Save the existing user so that the
                    # update page can use it if needed.

                    st.session_state[
                        "existing_user_to_update"
                    ] = matching_users[0]["user"].user_id

                    # Move to the update function

                    modify_user_page(engine)

                return

            # -------------------------------------------------
            # NO DUPLICATE
            # CREATE NEW USER
            # -------------------------------------------------

            result = connection.execute(
                text(
                    """
                    INSERT INTO users
                    (
                        user_name,
                        phone_number,
                        email,
                        max_loans
                    )
                    VALUES
                    (
                        :user_name,
                        :phone_number,
                        :email,
                        :max_loans
                    )
                    """
                ),
                {
                    "user_name": user_name,
                    "phone_number": phone_number,
                    "email": email,
                    "max_loans": max_loans
                }
            )

            # MySQL AUTO_INCREMENT generates the ID

            new_user_id = result.lastrowid

        # -----------------------------------------------------
        # SUCCESS
        # -----------------------------------------------------

        st.success(
            f"User created successfully! "
            f"User ID: {new_user_id}"
        )

    except Exception as error:

        st.error(
            f"Error creating user: {error}"
        )

    

#Create loan


# =========================================================
# CREATE LOAN PAGE
# =========================================================

def create_loan_page(engine):

    st.subheader("Create a New Loan")

    try:

        # -------------------------------------------------
        # GET AVAILABLE BOOKS AND USERS
        # -------------------------------------------------

        with engine.connect() as connection:

            # Get available books
            books_result = connection.execute(
                text("""
                    SELECT
                        isbn,
                        title,
                        author,
                        is_available
                    FROM books
                    WHERE is_available = TRUE
                    ORDER BY title
                """)
            )

            books = books_result.mappings().all()

            # Get users
            users_result = connection.execute(
                text("""
                    SELECT
                        user_id,
                        user_name,
                        max_loans
                    FROM users
                    ORDER BY user_name
                """)
            )

            users = users_result.mappings().all()

        # -------------------------------------------------
        # CHECK AVAILABLE BOOKS
        # -------------------------------------------------

        if not books:

            st.warning(
                "There are no available books to loan."
            )

            return

        # -------------------------------------------------
        # CHECK USERS
        # -------------------------------------------------

        if not users:

            st.warning(
                "There are no users available."
            )

            return

        # -------------------------------------------------
        # SELECT BOOK
        # -------------------------------------------------

        book_options = {
            f"{book['title']} — ISBN: {book['isbn']}": book
            for book in books
        }

        selected_book_label = st.selectbox(
            "Select Book",
            list(book_options.keys())
        )

        selected_book = book_options[
            selected_book_label
        ]

        # -------------------------------------------------
        # SELECT USER
        # -------------------------------------------------

        user_options = {
            f"{user['user_name']} — User ID: {user['user_id']}": user
            for user in users
        }

        selected_user_label = st.selectbox(
            "Select User",
            list(user_options.keys())
        )

        selected_user = user_options[
            selected_user_label
        ]

        # -------------------------------------------------
        # SHOW REMAINING LOANS
        # -------------------------------------------------

        st.write(
            f"**Remaining Loans:** "
            f"{selected_user['max_loans']}"
        )

        # -------------------------------------------------
        # CHECK LOAN LIMIT
        # -------------------------------------------------

        if selected_user["max_loans"] <= 0:

            st.error(
                f"{selected_user['user_name']} "
                f"has reached the maximum loan limit."
            )

            return

        # -------------------------------------------------
        # LOAN DATE
        # -------------------------------------------------

        loan_date = st.date_input(
            "Loan Date",
            value=date.today()
        )

        # -------------------------------------------------
        # AUTOMATIC DUE DATE
        #
        # Due date is ALWAYS exactly 20 days
        # after the loan date.
        # -------------------------------------------------

        due_date = (
            loan_date
            + timedelta(days=20)
        )

        # -------------------------------------------------
        # LOAN INFORMATION
        # -------------------------------------------------

        st.subheader("Loan Information")

        st.write(
            f"**Book:** {selected_book['title']}"
        )

        st.write(
            f"**ISBN:** {selected_book['isbn']}"
        )

        st.write(
            f"**User:** {selected_user['user_name']}"
        )

        st.write(
            f"**User ID:** {selected_user['user_id']}"
        )

        st.write(
            f"**Remaining Loans Before Borrowing:** "
            f"{selected_user['max_loans']}"
        )

        st.write(
            f"**Loan Date:** {loan_date}"
        )

        # -------------------------------------------------
        # AUTOMATIC DUE DATE DISPLAY
        #
        # User cannot manually change this.
        # -------------------------------------------------

        st.write(
            f"**Due Date:** {due_date}"
        )

        st.info(
            "The due date is automatically set to "
            "20 days after the loan date."
        )

        # -------------------------------------------------
        # CREATE LOAN BUTTON
        # -------------------------------------------------

        create_button = st.button(
            "Create Loan",
            type="primary"
        )

        if create_button:

            # -------------------------------------------------
            # CREATE LOAN
            #
            # Do NOT pass due_date.
            # create_loan() calculates it automatically.
            # -------------------------------------------------

            result = create_loan(
                engine=engine,
                isbn=selected_book["isbn"],
                user_id=selected_user["user_id"],
                loan_date=loan_date
            )

            # -------------------------------------------------
            # SUCCESS
            # -------------------------------------------------

            if result["success"]:

                st.success(
                    result["message"]
                )

                st.info(
                    f"Remaining loan allowance: "
                    f"{result['remaining_loans']}"
                )

            # -------------------------------------------------
            # ERROR
            # -------------------------------------------------

            else:

                st.error(
                    result["message"]
                )

    except Exception as error:

        st.error(
            f"Error loading loan page: {error}"
        )


# =========================================================
# CREATE LOAN
# =========================================================

def create_loan(
    engine,
    isbn,
    user_id,
    loan_date=None
):

    # -------------------------------------------------
    # LOAN DATE
    # -------------------------------------------------

    if loan_date is None:

        loan_date = date.today()

    # -------------------------------------------------
    # AUTOMATIC DUE DATE
    #
    # ALWAYS exactly 20 days after loan date.
    # -------------------------------------------------

    due_date = (
        loan_date
        + timedelta(days=20)
    )

    try:

        with engine.begin() as connection:

            # -------------------------------------------------
            # CHECK BOOK
            # -------------------------------------------------

            book = connection.execute(
                text("""
                    SELECT
                        isbn,
                        title,
                        is_available
                    FROM books
                    WHERE isbn = :isbn
                """),
                {
                    "isbn": isbn
                }
            ).mappings().first()

            if book is None:

                return {
                    "success": False,
                    "message": (
                        f"Book with ISBN {isbn} "
                        f"does not exist."
                    )
                }

            # -------------------------------------------------
            # CHECK WHETHER BOOK IS CURRENTLY LOANED
            # -------------------------------------------------

            active_loan = connection.execute(
                text("""
                    SELECT
                        l.loan_id,
                        l.user_id,
                        u.user_name,
                        l.loan_date,
                        l.due_date,
                        l.extended_due_date
                    FROM loans l

                    INNER JOIN users u
                        ON l.user_id = u.user_id

                    WHERE l.isbn = :isbn
                      AND l.return_date IS NULL

                    ORDER BY l.loan_id DESC
                    LIMIT 1
                """),
                {
                    "isbn": isbn
                }
            ).mappings().first()

            # -------------------------------------------------
            # BOOK IS ALREADY LOANED
            # -------------------------------------------------

            if active_loan is not None:

                current_due_date = (
                    active_loan["extended_due_date"]
                    if active_loan["extended_due_date"] is not None
                    else active_loan["due_date"]
                )

                return {
                    "success": False,
                    "book_loaned": True,
                    "message": (
                        f"'{book['title']}' is currently "
                        f"loaned to another user.\n\n"
                        f"Current due date: "
                        f"{current_due_date}.\n\n"
                        f"Please come back after "
                        f"{current_due_date} to borrow this book."
                    ),
                    "loan_id": active_loan["loan_id"],
                    "due_date": current_due_date
                }

            # -------------------------------------------------
            # CHECK BOOK AVAILABILITY
            # -------------------------------------------------

            if not book["is_available"]:

                return {
                    "success": False,
                    "book_loaned": True,
                    "message": (
                        f"'{book['title']}' is currently "
                        f"unavailable.\n\n"
                        f"Please come back after the current "
                        f"loan is returned."
                    )
                }

            # -------------------------------------------------
            # CHECK USER
            # -------------------------------------------------

            user = connection.execute(
                text("""
                    SELECT
                        user_id,
                        user_name,
                        max_loans
                    FROM users
                    WHERE user_id = :user_id
                """),
                {
                    "user_id": user_id
                }
            ).mappings().first()

            if user is None:

                return {
                    "success": False,
                    "message": (
                        f"User {user_id} "
                        f"does not exist."
                    )
                }

            # -------------------------------------------------
            # CHECK REMAINING LOAN ALLOWANCE
            # -------------------------------------------------

            if user["max_loans"] <= 0:

                return {
                    "success": False,
                    "message": (
                        f"{user['user_name']} has "
                        f"reached the maximum loan limit."
                    )
                }

            # -------------------------------------------------
            # INSERT LOAN
            #
            # Due date is automatically calculated
            # as loan_date + 20 days.
            # -------------------------------------------------

            result = connection.execute(
                text("""
                    INSERT INTO loans (
                        isbn,
                        user_id,
                        loan_date,
                        due_date,
                        extended_due_date,
                        extension_count,
                        late_fee,
                        return_date,
                        fine_paid_date
                    )
                    VALUES (
                        :isbn,
                        :user_id,
                        :loan_date,
                        :due_date,
                        NULL,
                        0,
                        0.00,
                        NULL,
                        NULL
                    )
                """),
                {
                    "isbn": isbn,
                    "user_id": user_id,
                    "loan_date": loan_date,
                    "due_date": due_date
                }
            )

            loan_id = result.lastrowid

            # -------------------------------------------------
            # DECREASE USER'S REMAINING LOANS
            # -------------------------------------------------

            connection.execute(
                text("""
                    UPDATE users
                    SET max_loans = max_loans - 1
                    WHERE user_id = :user_id
                      AND max_loans > 0
                """),
                {
                    "user_id": user_id
                }
            )

            # -------------------------------------------------
            # GET UPDATED REMAINING LOANS
            # -------------------------------------------------

            remaining_loans = connection.execute(
                text("""
                    SELECT max_loans
                    FROM users
                    WHERE user_id = :user_id
                """),
                {
                    "user_id": user_id
                }
            ).scalar()

            # -------------------------------------------------
            # MARK BOOK AS UNAVAILABLE
            # -------------------------------------------------

            connection.execute(
                text("""
                    UPDATE books
                    SET is_available = FALSE
                    WHERE isbn = :isbn
                """),
                {
                    "isbn": isbn
                }
            )

        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        return {
            "success": True,
            "book_loaned": False,

            "message": (
                f"Loan created successfully!\n\n"
                f"Loan ID: {loan_id}\n"
                f"Book: {book['title']}\n"
                f"User: {user['user_name']}\n"
                f"Loan date: {loan_date}\n"
                f"Due date: {due_date}\n\n"
                f"Remaining loan allowance: "
                f"{remaining_loans}"
            ),

            "loan_id": loan_id,
            "remaining_loans": remaining_loans,
            "due_date": due_date
        }

    except Exception as error:

        print(
            "Database error:",
            error
        )

        return {
            "success": False,
            "book_loaned": False,
            "message": (
                f"Error creating loan: {error}"
            )
        }