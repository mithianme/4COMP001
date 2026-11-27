from datetime import date

import storage


def test_load_data_with_no_file_yet(tmp_path):
    assert storage.load_data(tmp_path / "test_data.json") == {}


def test_create_account_and_get_user(tmp_path):
    file = tmp_path / "test_data.json"
    assert storage.get_user("tester1", file) is None
    storage.create_account("tester1", "a-hash", file)
    user = storage.get_user("tester1", file)
    assert user["password_hash"] == "a-hash"
    assert user["weekly_budget"] == 0
    assert user["spending"] == []


def test_set_budget(tmp_path):
    file = tmp_path / "test_data.json"
    storage.create_account("tester1", "a-hash", file)
    storage.set_budget("tester1", 60, file)
    assert storage.get_user("tester1", file)["weekly_budget"] == 60


def test_add_and_delete_spending(tmp_path):
    file = tmp_path / "test_data.json"
    storage.create_account("tester1", "a-hash", file)
    storage.add_spending("tester1", 4.5, "Food", date(2026, 12, 1), " Meal deal ", file)
    storage.add_spending("tester1", 2.0, "Transport", date(2026, 12, 2), "", file)
    spending = storage.get_user("tester1", file)["spending"]
    assert len(spending) == 2
    assert spending[0]["date"] == "2026-12-01" 
    assert spending[0]["note"] == "Meal deal"  

    assert storage.delete_spending("tester1", 1, file) is True
    assert storage.delete_spending("tester1", 1, file) is False 
    assert len(storage.get_user("tester1", file)["spending"]) == 1


def test_ids_never_repeat_after_a_delete(tmp_path):
    file = tmp_path / "test_data.json"
    storage.create_account("tester1", "a-hash", file)
    storage.add_spending("tester1", 1.0, "Food", date(2026, 12, 1), "", file)
    storage.add_spending("tester1", 2.0, "Food", date(2026, 12, 1), "", file)
    storage.delete_spending("tester1", 1, file)
    storage.add_spending("tester1", 3.0, "Other", date(2026, 12, 2), "Pens", file)
    ids = [item["id"] for item in storage.get_user("tester1", file)["spending"]]
    assert ids == [2, 3] 