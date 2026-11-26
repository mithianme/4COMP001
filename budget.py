import hashlib
import math

CATEGORIES = ["Food", "Transport", "Going out", "Shopping", "Bills", "Course costs", "Other"]

AMOUNT_MAX = 1000  # the biggest amount of spending we accept, in pounds


def money(amount):
    """Show an amount the way people write money: 4.5 becomes '£4.50'."""
    return f"£{amount:.2f}"


def read_money(text):
    """Turn what the user typed into a number, for example '£4.50' becomes 4.5.

    Gives back None if what they typed is not a number.
    """
    text = text.strip().replace("£", "")
    try:
        amount = round(float(text), 2)
    except ValueError:
        return None
    if not math.isfinite(amount):  
        return None
    return amount


def check_amount(text, biggest):
    """Check an amount typed by the user. Gives back a list of problems (an empty list means it is fine)."""
    amount = read_money(text)
    if amount is None:
        return ["Please type the amount as a number, for example 4.50."]
    if amount <= 0:
        return ["The amount must be more than £0."]
    if amount > biggest:
        return [f"The amount must be {money(biggest)} or less."]
    return []


def check_spending(amount_text, category, spent_on, today):
    """Check everything on the Add spending form. Gives back a list of problems."""
    problems = check_amount(amount_text, AMOUNT_MAX)
    if category not in CATEGORIES:
        problems.append("Please choose a category.")
    if spent_on > today:
        problems.append("The date cannot be in the future.")
    return problems

def clean_username(username):
    """This tidies the username, removes spaces at the ends and use small letters."""
    return username.strip().lower()


def check_new_account(username, password, password_again, taken_usernames):
    """Check the create an account form, gives back a list of problems."""
    problems = []
    username = clean_username(username)
    if len(username) < 3 or len(username) > 20 or not username.isalnum():
        problems.append("Your username must be 3 to 20 letters and numbers with no spaces.")
    elif username in taken_usernames:
        problems.append("That username is already taken, please choose another one.")
    if len(password) < 8:
        problems.append("Your password must be at least 8 characters long.")
    elif password != password_again:
        problems.append("The two passwords are not the same.")
    return problems


def hash_password(password):
    """Srambling password with SHA-256, so the real password is never saved anywhere."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def week_start(today):
    pass


def spending_this_week(spending, today):
    pass


def total(spending):
    pass


def totals_by_category(spending):
    pass


def budget_status(spent, weekly_budget):
    pass
