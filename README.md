# Student Budget Tracker

A website that helps students keep track of their weekly spending, so that their money lasts until the next loan payment.

Software Development (COMP4-02555), Assignment 2 - Group Coursework, Canterbury Christ Church University.

**Live app:** https://student-budget-tracker2026.streamlit.app/

## Live Application

1. Open the link above and choose **Create an account**. Any username and password will do (please don't use a real password).
2. Set a **Weekly budget**, add some spending, then look at **This week**.

The live app saves its data in a file on Streamlit's server. That file gets wiped whenever the app restarts or we update it, so accounts made on the live app arent permanent. If the app has gone to sleep, click **"Yes, get this app back up"** and wait a minute.

## What it does

- **Create an account, log in and log out.** Passwords are scrambled (hashed with SHA-256) before they are saved, so the real password is never actually stored.
- **Weekly budget:** set how much you want to spend each week (up to £2000).
- **Add spending:** the amount (up to £1000), a category, the date and an optional note. It refuses amounts that aren't numbers, amounts of £0 or less, and dates that are in the future.
- **This week:** your budget, what you've spent and what's left, with a message that tells you how you're doing, and a bar chart of where your money went. Runs from Monday to Sunday.
  - Blue: you haven't set a budget yet.
  - Green: you're within your budget.
  - Orange: you've used 80% or more of your budget.
  - Red: you're over your budget, and by how much.
- **My spending:** everything you've spent, with an option to delete a mistake (coming in Sprint 2).

## What you need

- Python 3.13 (the version we used)
- Streamlit 1.67.0 (listed in `requirements.txt`)
- For the tests and code checks: pytest and Ruff

## How to install and run it

1. Download this repository or clone it. On GitHub, click the green **Code** button, then **Open with GitHub Desktop** (or **Download ZIP** and unzip it using 7zip or WinRAR).
2. Open the folder in VS Code, then open a terminal (**Terminal > New Terminal**).
3. Install what it needs:

   ```
   python -m pip install -r requirements.txt pytest ruff
   ```

4. Start the app:

   ```
   python -m streamlit run app.py
   ```

5. Your browser opens the app at http://localhost:8501. If you want to stop it, click in the terminal and press **Ctrl + C**.

## How to use it

1. Choose **Create an account**. Pick a username (3 to 20 letters and numbers) and a password (at least 8 characters).
2. On the left, choose **Weekly budget** and type how much you want to spend each week, for example `60`.
3. Each time you spend money, choose **Add spending**, type the amount (`4.50` or `£4.50`), choose a category and press **Add spending**.
4. **This week** shows how much you have left and where your money went.
5. Press **Log out** on the left when you're done.

## How to run the tests and the code checks

```
python -m pytest            # runs the automated tests in the tests folder
python -m ruff check .      # looks for mistakes and style problems
```

## How the code is organised

| File | What it does |
|---|---|
| `app.py` | Everything you see: the pages, forms and messages |
| `budget.py` | The rules and the sums: checking what people type, this week's total, the budget warning |
| `storage.py` | Saves and loads everything in `budget_data.json` |
| `.streamlit/config.toml` | The app's colours (Maite's "Underwater Scene" palette) |
| `requirements.txt` | What the app needs to run |
| `ruff.toml`, `pytest.ini` | Settings for Ruff and pytest |

The data is kept in `budget_data.json`, which is made the first time someone creates an account. It's listed in `.gitignore`, so data never goes on GitHub.

## Our project documents

| Folder or file | What's in it |
|---|---|
| `docs/requirements.docx` | The problem, who the app is for, the requirements and why we used Agile (Hena) |
| `docs/Research for Asssignment 2.md` | The facts and sources behind the problem (Glenn) |
| `docs/design` | The use case, architecture and activity diagrams, and the screen designs (Maite and Ollie) |
| `docs/testing` | The manual test plan, the developer checks and their screenshots (Archie, Ollie and Vlad) |
| `docs/meeting-notes.md` | Our team meeting notes (Hena and Glenn) |
| `docs/trello` | Screenshots of our Trello board at the start of each sprint (Hena) |
| `docs/ai-log.md` | Where and how we used AI tools (Everyone) |

## Our team

| Role | Name |
|---|---|
| Organiser | Hena Dale |
| Researcher | Glenn Chitepo |
| Designer | Maite Matthews |
| Lead Coder | Oliver Peploe |
| Tester | Archie Gardner |
| Manual Tester | Vlad Diaconescu |
