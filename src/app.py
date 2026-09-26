import streamlit as st
from sqlalchemy import create_engine, text

from create import *
from read import *
from update import *
from delete import *


# =========================================================
# DATABASE CONNECTION
# =========================================================

db_user = "root"
db_host = "127.0.0.1"
db_port = 3306
db_name = "library"

sql_pass = st.secrets["mysql"]["password"]

connection_string = (
    f"mysql+pymysql://{db_user}:{sql_pass}"
    f"@{db_host}:{db_port}/{db_name}"
)

if (
    "engine" not in st.session_state
    or st.session_state["engine"] is None
):

    st.session_state["engine"] = create_engine(
        connection_string,
        pool_pre_ping=True
    )

engine = st.session_state["engine"]


if engine is None:

    st.error(
        "Database engine was not created."
    )

    st.stop()


# =========================================================
# PAGE STYLING
# =========================================================

st.markdown(
    """
    <style>

    /* ---------------------------------------------
       Main application background
       --------------------------------------------- */

    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }


    /* ---------------------------------------------
       Main headings
       --------------------------------------------- */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: var(--text-color) !important;
    }


    /* ---------------------------------------------
       Normal text
       --------------------------------------------- */

    p,
    label {
        color: var(--text-color);
    }


    /* ---------------------------------------------
       Metrics
       --------------------------------------------- */

    [data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-color) !important;
    }


    /* ---------------------------------------------
       Sidebar
       --------------------------------------------- */

    [data-testid="stSidebar"] {
        background-color: var(--secondary-background-color);
    }


    /* ---------------------------------------------
       Sidebar text
       --------------------------------------------- */

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: var(--text-color);
    }


    /* ---------------------------------------------
       Input labels
       --------------------------------------------- */

    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stDateInput"] label,
    [data-testid="stSelectbox"] label {
        color: var(--text-color) !important;
    }


    /* ---------------------------------------------
       Alert messages
       Let Streamlit control their background
       and normal alert colors.
       --------------------------------------------- */

    [data-testid="stAlert"] {
        color: var(--text-color);
    }


    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# APPLICATION TITLE
# =========================================================

st.title(
    "Library Management System for Liana",
    text_alignment="center"
)


# =========================================================
# MAIN NAVIGATION
# =========================================================

st.sidebar.title("Library App")

section = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Books Details",
        "User Details",
        "Loan Details"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if section == "Dashboard":

    st.header("Dashboard")

    try:

        with engine.connect() as connection:

            # ---------------------------------------------
            # TOTAL BOOKS
            # ---------------------------------------------

            total_books = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM books
                """)
            ).scalar()

            # ---------------------------------------------
            # TOTAL USERS
            # ---------------------------------------------

            total_users = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM users
                """)
            ).scalar()

            # ---------------------------------------------
            # ACTIVE LOANS
            # ---------------------------------------------

            active_loans = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM loans
                    WHERE return_date IS NULL
                """)
            ).scalar()

            # ---------------------------------------------
            # OVERDUE LOANS
            # ---------------------------------------------

            overdue_loans = connection.execute(
                text("""
                    SELECT COUNT(*)
                    FROM loans
                    WHERE return_date IS NULL
                    AND COALESCE(
                        extended_due_date,
                        due_date
                    ) < CURRENT_DATE
                """)
            ).scalar()

        # ---------------------------------------------
        # DISPLAY METRICS
        # ---------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Total Books",
                total_books
            )

        with col2:

            st.metric(
                "Total Users",
                total_users
            )

        with col3:

            st.metric(
                "Active Loans",
                active_loans
            )

        with col4:

            st.metric(
                "Overdue Loans",
                overdue_loans
            )

    except Exception as error:

        st.error(
            f"Could not load dashboard: {error}"
        )


# =========================================================
# BOOKS DETAILS
# =========================================================

elif section == "Books Details":

    book_action = st.sidebar.radio(
        "Books Details",
        [
            "Create a new book",
            "Modify a book",
            "Delete a book",
            "Read book details"
        ]
    )

    # ---------------------------------------------
    # CREATE BOOK
    # ---------------------------------------------

    if book_action == "Create a new book":

        create_book_page(engine)

    # ---------------------------------------------
    # MODIFY BOOK
    # ---------------------------------------------

    elif book_action == "Modify a book":

        modify_book_page(engine)

    # ---------------------------------------------
    # DELETE BOOK
    # ---------------------------------------------

    elif book_action == "Delete a book":

        delete_book_page(engine)

    # ---------------------------------------------
    # READ BOOK
    # ---------------------------------------------

    elif book_action == "Read book details":

        read_book_page(engine)


# =========================================================
# USER DETAILS
# =========================================================

elif section == "User Details":

    user_action = st.sidebar.radio(
        "User Details",
        [
            "Create a new user",
            "Modify an existing user",
            "Delete a user",
            "Read user details"
        ]
    )

    # ---------------------------------------------
    # CREATE USER
    # ---------------------------------------------

    if user_action == "Create a new user":

        create_user_page(engine)

    # ---------------------------------------------
    # MODIFY USER
    # ---------------------------------------------

    elif user_action == "Modify an existing user":

        modify_user_page(engine)

    # ---------------------------------------------
    # DELETE USER
    # ---------------------------------------------

    elif user_action == "Delete a user":

        delete_user_page(engine)

    # ---------------------------------------------
    # READ USER
    # ---------------------------------------------

    elif user_action == "Read user details":

        read_user_page(engine)


# =========================================================
# LOAN DETAILS
# =========================================================

elif section == "Loan Details":

    loan_action = st.sidebar.radio(
        "Loan Details",
        [
            "Create a new loan",
            "Modify an existing loan",
            "Read loan details"
        ]
    )

    # ---------------------------------------------
    # CREATE LOAN
    # ---------------------------------------------

    if loan_action == "Create a new loan":

        create_loan_page(engine)

    # ---------------------------------------------
    # MODIFY LOAN
    # ---------------------------------------------

    elif loan_action == "Modify an existing loan":

        modify_loan_page(engine)

    # ---------------------------------------------
    # READ LOAN
    # ---------------------------------------------

    elif loan_action == "Read loan details":

        read_loan_page(engine)