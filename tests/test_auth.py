import os
from pathlib import Path
import pytest

from recommender.auth import (
    authenticate_user,
    create_user_session,
    delete_user_session,
    get_saved_trips,
    get_saved_trips_count,
    get_user_by_session,
    is_trip_saved,
    register_user,
    remove_saved_trip,
    save_trip,
)


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_auth.db"
    return db_file


def test_register_and_authenticate(temp_db):
    user, err = register_user("testuser", "test@example.com", "secret123", full_name="Test User", db_path=temp_db)
    assert err is None
    assert user["username"] == "testuser"
    assert user["email"] == "test@example.com"
    assert user["full_name"] == "Test User"

    # Authenticate with username
    auth_user, auth_err = authenticate_user("testuser", "secret123", db_path=temp_db)
    assert auth_err is None
    assert auth_user["id"] == user["id"]

    # Authenticate with email
    auth_user2, auth_err2 = authenticate_user("test@example.com", "secret123", db_path=temp_db)
    assert auth_err2 is None
    assert auth_user2["id"] == user["id"]

    # Wrong password
    bad_user, bad_err = authenticate_user("testuser", "wrongpwd", db_path=temp_db)
    assert bad_user is None
    assert "Invalid" in bad_err


def test_duplicate_registration_rejected(temp_db):
    user, err = register_user("alex", "alex@example.com", "pass1234", db_path=temp_db)
    assert err is None

    # Duplicate username
    dup_user, dup_err = register_user("alex", "other@example.com", "pass1234", db_path=temp_db)
    assert dup_user is None
    assert "username is already taken" in dup_err.lower()

    # Duplicate email
    dup_user2, dup_err2 = register_user("alex2", "alex@example.com", "pass1234", db_path=temp_db)
    assert dup_user2 is None
    assert "already exists" in dup_err2.lower()


def test_saved_trips(temp_db):
    user, _ = register_user("traveler", "traveler@example.com", "pass1234", db_path=temp_db)
    uid = user["id"]

    assert get_saved_trips_count(uid, db_path=temp_db) == 0
    assert not is_trip_saved(uid, "Kyoto", db_path=temp_db)

    # Save trips
    save_trip(uid, "Kyoto", "Japan", db_path=temp_db)
    save_trip(uid, "Bagan", "Myanmar", db_path=temp_db)

    assert get_saved_trips_count(uid, db_path=temp_db) == 2
    assert is_trip_saved(uid, "Kyoto", db_path=temp_db)
    assert is_trip_saved(uid, "Bagan", db_path=temp_db)

    trips = get_saved_trips(uid, db_path=temp_db)
    assert len(trips) == 2
    names = [t["destination_name"] for t in trips]
    assert "Kyoto" in names
    assert "Bagan" in names

    # Remove trip
    remove_saved_trip(uid, "Kyoto", db_path=temp_db)
    assert get_saved_trips_count(uid, db_path=temp_db) == 1
    assert not is_trip_saved(uid, "Kyoto", db_path=temp_db)
    assert is_trip_saved(uid, "Bagan", db_path=temp_db)


def test_user_session_persistence(temp_db):
    user, _ = register_user("session_user", "session@example.com", "pass1234", full_name="Session Traveler", db_path=temp_db)
    uid = user["id"]

    token = create_user_session(uid, days_valid=7, db_path=temp_db)
    assert token is not None and len(token) > 10

    # Retrieve user by token
    restored = get_user_by_session(token, db_path=temp_db)
    assert restored is not None
    assert restored["id"] == uid
    assert restored["username"] == "session_user"
    assert restored["full_name"] == "Session Traveler"

    # Delete session (Logout)
    assert delete_user_session(token, db_path=temp_db) is True
    assert get_user_by_session(token, db_path=temp_db) is None

