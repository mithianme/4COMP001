# Developer checks

Checks I ran in the terminal while building each part, before committing.
Archie's automated tests will be in `tests/` and Vlad's manual tests will be in `docs/testing`.

## Card 11: storage.py (25th November 2026)

Tested with a test user, oliver01, and a test file, `try.json`, which I deleted afterwards.

| # | What I checked | What should happen | Result |
|---|---|---|---|
| 1 | `load_data` when there is no file yet | Gives back `{}` | Pass |
| 2 | `get_user` for a user who doesn't exist | Gives back `None` (nothing is shown) | Pass |
| 3 | `create_account` for oliver01 | Saves the user with a weekly budget of 0 and no spending | Pass |
| 4 | `set_budget` to 60 | `get_user` now shows a weekly budget of 60 | Pass |
| 5 | `add_spending` twice (£4.50 Food with the note " Meal deal ", then £2 Transport) | Two entries with ids 1 and 2, the dates saved as text, and the note trimmed to "Meal deal" | Pass |
| 6 | `delete_spending` entry 1 | Gives back `True` | Pass |
| 7 | `delete_spending` entry 1 again | Gives back `False`, because it has already gone | Pass |
| 8 | `add_spending` after the delete (£3 Other, "Pens") | The new entry gets id 3, not 2 (last id + 1), so ids never repeat | Pass |

Screenshot: `screenshots/card-11-storage-check.png`

Ruff (`python -m ruff check`): all checks passed.

## Card 12: Log in and Create an account (25th November 2026)

All checks were tested in the browser by running the app on my laptop (`python -m streamlit run app.py`).

| # | What I checked | What should happen | Result |
|---|---|---|---|
| 1 | Ruff on `budget.py` after commit 1 | No problems | **Bug found:** Ruff said `hashlib` wasn't imported (F821), so creating an account would have crashed. I added `import hashlib` (commit e23735e) and Ruff then passed |
| 2 | Create an account with a 7-character password | Red message: at least 8 characters | Pass: "Your password must be at least 8 characters long." |
| 3 | Create an account with two different passwords | Red message: the passwords are not the same | Pass: "The two passwords are not the same." |
| 4 | Create the account oliver01 properly | Logged in straight away, with the menu on the left | Pass |
| 5 | Create Oliver01 (with a capital) when oliver01 already exists | Red message: that username is already taken | Pass |
| 6 | Log in with the wrong password | Red message: the username or password is not right | Pass: "The username or password is not right." |
| 7 | Log in as oliver01 with the right password | Logged in, with the menu on the left | Pass |

Screenshots: `screenshots/card-12-username-check.png` (check 5) and `screenshots/card-12-login-check.png` (check 7)

Ruff (`python -m ruff check`): all checks passed.

## Card 13: Add spending page and the amount checks (26th November 2026)

All checks were tested in the browser by running the app on my laptop (`python -m streamlit run app.py`), logged in as oliver01.

| # | What I checked | What should happen | Result |
|---|---|---|---|
| 1 | Add spending with the amount `abc` | Red message: type the amount as a number | Pass: "Please type the amount as a number, for example 4.50." |
| 2 | Add spending with the amount `0` | Red message: the amount must be more than £0 | Pass: "The amount must be more than £0." |
| 3 | Add spending of `5` without choosing a category | Red message: choose a category | Pass: "Please choose a category." |
| 4 | Add spending of `5`, Food, with tomorrow's date | Red message: the date can't be in the future | Pass: "The date cannot be in the future." |
| 5 | Add spending of `4.50`, Food, today, with the note "Meal deal" | Green message, and the form clears | Pass: "Added £4.50 for Food." |
| 6 | Press Log out in the menu on the left | Back to the Log in page | Pass |

Ruff (`python -m ruff check`): all checks passed.

## Cards 14, 15 and 16: This week's sums, the This week page and the Weekly budget page (27th November 2026)

These checks were run on 27th November with Streamlit's test tool

| # | What I checked | What should happen | Result |
|---|---|---|---|
| 1 | Ruff after card 14 | No problems | Ruff said the imports in `budget.py` weren't in the right order (I001). Fixed in commit 854a88a, then Ruff passed |
| 2 | Ruff after card 15, part 1 | No problems | Ruff said `status` was worked out but never used (F841). That showed the coloured message was missing from the This week page. Added the message and the bar chart in commit 9e0d48f, then Ruff passed |
| 3 | This week with £12.50 spent this Monday and £99 spent last Sunday | Only this week's spending counts | Pass: "Spent this week" shows £12.50 |
| 4 | This week with no budget set | Blue message | Pass: "You have not set a weekly budget yet. Choose Weekly budget on the left." |
| 5 | This week with £12.50 spent out of £60 | Green message, and £47.50 left | Pass: "You are within your budget. Nice one!" |
| 6 | This week with £16.50 spent out of £20 (82%) | Orange message | Pass: "You have used 80% or more of your budget. Go carefully until Monday." |
| 7 | This week with £26.50 spent out of £20 | Red message saying how much over, and £0.00 left (never below zero) | Pass: "You are £6.50 over your budget this week." and "Left to spend" shows £0.00 |
| 8 | This week after adding £4.50 for Food | The bar chart shows under "Where your money went this week" | Pass |
| 9 | Weekly budget: `0` | Red message | Pass: "The amount must be more than £0." |
| 10 | Weekly budget: `abc` | Red message | Pass: "Please type the amount as a number, for example 4.50." |
| 11 | Weekly budget: `2500` (over the £2000 limit) | Red message | Pass: "The amount must be £2000.00 or less." |
| 12 | Weekly budget: `60` | Saved, and the page shows the new budget | Pass: "Saved." and "Your weekly budget is £60.00." |

Screenshots: `screenshots/card-15-this-week-check.png` (checks 6 and 8) and `screenshots/card-16-budget-check.png` (check 12)

Ruff (`python -m ruff check`): all checks passed.

## Card 19: Putting the app online (27th November 2026)

The app is on Streamlit Community Cloud: https://student-budget-tracker2026.streamlit.app/

Checked in the browser on the live link on 27th November

| # | What I checked | What should happen | Result |
|---|---|---|---|
| 1 | Open the live link | The Log in page loads, with Maite's colours | Pass |
| 2 | Create an account on the live app | Logged in straight away, with the blue "not set" message on This week | Pass |

Screenshot: `screenshots/card-19-live-check.png` (check 2)

The live app saves its data in a file on Streamlit's server, which is wiped when the app restarts or is updated. We'll write about this as a limitation in the report.
