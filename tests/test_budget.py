from datetime import date

import budget

TODAY = date(2026, 12, 2) 

def entry(day, amount, category="Food"):
    """Make one spending entry for a test."""
    return {"id": 1, "date": day.isoformat(), "category": category, "amount": amount, "note": ""}


def test_money_shows_two_decimal_places():
    assert budget.money(4.5) == "£4.50"
    assert budget.money(1000) == "£1000.00"


def test_read_money_normal():
    assert budget.read_money("4.50") == 4.5


def test_read_money_with_pound_sign_and_spaces():
    assert budget.read_money(" £4.50 ") == 4.5


def test_read_money_not_a_number():
    assert budget.read_money("abc") is None
    assert budget.read_money("") is None


def test_read_money_refuses_nan_and_inf():
    assert budget.read_money("nan") is None
    assert budget.read_money("inf") is None


def test_check_amount_messages():
    assert budget.check_amount("abc", 1000) == ["Please type the amount as a number, for example 4.50."]
    assert budget.check_amount("0", 1000) == ["The amount must be more than £0."]
    assert budget.check_amount("-5", 1000) == ["The amount must be more than £0."]
    assert budget.check_amount("1000.01", 1000) == ["The amount must be £1000.00 or less."]


def test_check_amount_boundaries():
    assert budget.check_amount("0.01", 1000) == []  
    assert budget.check_amount("1000", 1000) == []  
    assert budget.check_amount("2000", budget.BUDGET_MAX) == []  
    assert budget.check_amount("2000.01", budget.BUDGET_MAX) == ["The amount must be £2000.00 or less."]


def test_check_spending_all_fine():
    assert budget.check_spending("4.50", "Food", TODAY, TODAY) == []


def test_check_spending_future_date():
    tomorrow = date(2026, 12, 3)
    assert budget.check_spending("4.50", "Food", tomorrow, TODAY) == ["The date cannot be in the future."]


def test_check_spending_no_category():
    assert budget.check_spending("4.50", None, TODAY, TODAY) == ["Please choose a category."]

def test_clean_username():
    assert budget.clean_username("  Archie01 ") == "archie01"


def test_username_must_be_3_to_20_letters_and_numbers():
    problem = "Your username must be 3 to 20 letters and numbers with no spaces."
    assert budget.check_new_account("ab", "password1", "password1", []) == [problem]
    assert budget.check_new_account("arc hie", "password1", "password1", []) == [problem]
    assert budget.check_new_account("abc", "password1", "password1", []) == []


def test_taken_username_with_capitals_is_rejected():
    problems = budget.check_new_account("Archie01", "password1", "password1", ["archie01"])
    assert problems == ["That username is already taken, please choose another one."]


def test_password_must_be_at_least_8_characters():
    assert budget.check_new_account("tester1", "pass123", "pass123", []) == [
        "Your password must be at least 8 characters long."
    ]
    assert budget.check_new_account("tester1", "pass1234", "pass1234", []) == [] 


def test_passwords_must_match():
    problems = budget.check_new_account("tester1", "password1", "password2", [])
    assert problems == ["The two passwords are not the same."]


def test_hash_password():
    hashed = budget.hash_password("password1")
    assert hashed != "password1" 
    assert hashed == budget.hash_password("password1")  
    assert hashed != budget.hash_password("password2")


def test_week_starts_on_monday():
    assert budget.week_start(TODAY) == date(2026, 11, 30)
    assert budget.week_start(date(2026, 11, 30)) == date(2026, 11, 30) 


def test_last_sunday_does_not_count_this_week():
    last_sunday = date(2026, 11, 29)
    monday = date(2026, 11, 30)
    this_week = budget.spending_this_week([entry(last_sunday, 5), entry(monday, 3)], TODAY)
    assert this_week == [entry(monday, 3)]


def test_totals():
    spending = [entry(TODAY, 4.5), entry(TODAY, 2.25, "Transport"), entry(TODAY, 1.25)]
    assert budget.total(spending) == 8.0
    assert budget.total([]) == 0
    assert budget.totals_by_category(spending) == {"Food": 5.75, "Transport": 2.25}


def test_budget_status():
    assert budget.budget_status(10, 0) == "not set"
    assert budget.budget_status(47.99, 60) == "ok"
    assert budget.budget_status(48, 60) == "nearly" 
    assert budget.budget_status(60, 60) == "nearly"  
    assert budget.budget_status(60.01, 60) == "over"
