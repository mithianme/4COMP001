from datetime import date

import streamlit as st

import budget
import storage


def show_log_in():
    """The Log in and Create an account forms, shown until someone logs in."""
    st.write("Keep track of what you spend each week, so your money lasts until the next loan payment.")
    log_in_tab, sign_up_tab = st.tabs(["Log in", "Create an account"])

    with log_in_tab:
        with st.form("log_in_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            pressed = st.form_submit_button("Log in", type="primary")
        if pressed:
            username = budget.clean_username(username)
            user = storage.get_user(username)
            if user is not None and user["password_hash"] == budget.hash_password(password):
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("The username or password is not right.")

    with sign_up_tab:
        with st.form("sign_up_form"):
            new_username = st.text_input("Choose a username", help="3 to 20 letters and numbers")
            new_password = st.text_input("Choose a password", type="password", help="At least 8 characters")
            password_again = st.text_input("Type the password again", type="password")
            pressed = st.form_submit_button("Create account", type="primary")
        if pressed:
            taken = storage.load_data().keys()
            problems = budget.check_new_account(new_username, new_password, password_again, taken)
            if len(problems) > 0:
                for problem in problems:
                    st.error(problem)
            else:
                username = budget.clean_username(new_username)
                storage.create_account(username, budget.hash_password(new_password))
                st.session_state["username"] = username
                st.rerun()


def show_this_week(username):
    """This week's budget, spending and money left, with a coloured message and a bar chart."""
    user = storage.get_user(username)
    today = date.today()
    this_week = budget.spending_this_week(user["spending"], today)
    spent = budget.total(this_week)
    weekly_budget = user["weekly_budget"]
    status = budget.budget_status(spent, weekly_budget)

    st.subheader(f"Hi {username}, here is your week")
    col1, col2, col3 = st.columns(3)
    col1.metric("Weekly budget", budget.money(weekly_budget))
    col2.metric("Spent this week", budget.money(spent))
    col3.metric("Left to spend", budget.money(max(weekly_budget - spent, 0)))

    if status == "not set":
        st.info("You have not set a weekly budget yet. Choose Weekly budget on the left.")
    elif status == "over":
        st.error(f"You are {budget.money(spent - weekly_budget)} over your budget this week.")
    elif status == "nearly":
        st.warning("You have used 80% or more of your budget. Go carefully until Monday.")
    else:
        st.success("You are within your budget.")

    if len(this_week) > 0:
        st.subheader("Where your money went this week")
        totals = budget.totals_by_category(this_week)
        chart_data = {"Category": list(totals.keys()), "Spent (£)": list(totals.values())}
        st.bar_chart(chart_data, x="Category", y="Spent (£)")


def show_add_spending(username):
    """The form for adding something the student spent money on."""
    st.subheader("Add spending")
    with st.form("add_form", clear_on_submit=True):
        amount_text = st.text_input("Amount (£)", placeholder="For example 4.50")
        category = st.selectbox("Category", budget.CATEGORIES, index=None, placeholder="Choose a category")
        spent_on = st.date_input("Date", value=date.today(), format="DD/MM/YYYY")
        note = st.text_input("Note (optional)", max_chars=50, placeholder="For example: Meal deal")
        pressed = st.form_submit_button("Add spending", type="primary")

    if pressed:
        problems = budget.check_spending(amount_text, category, spent_on, date.today())
        if len(problems) > 0:
            for problem in problems:
                st.error(problem)
        else:
            amount = budget.read_money(amount_text)
            storage.add_spending(username, amount, category, spent_on, note)
            st.success(f"Added {budget.money(amount)} for {category}.")


def show_my_spending(username):
    st.write("My spending page: coming soon.")


def show_weekly_budget(username):
    """The form for setting how much the student wants to spend each week."""
    st.subheader("Weekly budget")
    st.write("How much do you want to spend each week on things like food, travel and going out?")
    with st.form("budget_form"):
        budget_text = st.text_input("Weekly budget (£)", placeholder="For example 60")
        pressed = st.form_submit_button("Save budget", type="primary")
    if pressed:
        problems = budget.check_amount(budget_text, budget.BUDGET_MAX)
        if len(problems) > 0:
            st.error(problems[0])
        else:
            storage.set_budget(username, budget.read_money(budget_text))
            st.success("Saved.")
    user = storage.get_user(username)
    st.write(f"Your weekly budget is **{budget.money(user['weekly_budget'])}**.")


st.title("Student Budget Tracker")

username = st.session_state.get("username")

if username is None:
    show_log_in()
else:
    page = st.sidebar.radio("Go to", ["This week", "Add spending", "My spending", "Weekly budget"])
    if st.sidebar.button("Log out"):
        st.session_state["username"] = None
        st.rerun()
    if page == "This week":
        show_this_week(username)
    elif page == "Add spending":
        show_add_spending(username)
    elif page == "My spending":
        show_my_spending(username)
    else:
        show_weekly_budget(username)
