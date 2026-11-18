from datetime import datetime, timedelta, timezone
import hashlib
import os
from pathlib import Path
import re
import secrets
import sqlite3

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "tripsense.db"


def get_db_connection(db_path=None):
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None):
    conn = get_db_connection(db_path)
    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS saved_trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                destination_name TEXT NOT NULL,
                country TEXT NOT NULL,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, destination_name),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
    conn.close()


def _hash_password(password: str, salt: bytes) -> str:
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000,
    )
    return key.hex()


def register_user(username: str, email: str, password: str, full_name: str = None, db_path=None):
    init_db(db_path)
    clean_username = (username or "").strip()
    clean_email = (email or "").strip().lower()
    clean_name = (full_name or "").strip() or clean_username

    if not clean_username or len(clean_username) < 3:
        return None, "Username must be at least 3 characters long."
    if not re.match(r"^[\w.-]+$", clean_username):
        return None, "Username can only contain letters, numbers, dots, and hyphens."
    if not clean_email or "@" not in clean_email or "." not in clean_email:
        return None, "Please enter a valid email address."
    if not password or len(password) < 6:
        return None, "Password must be at least 6 characters long."

    salt = os.urandom(16)
    pwd_hash = _hash_password(password, salt)

    conn = get_db_connection(db_path)
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, salt, full_name)
                VALUES (?, ?, ?, ?, ?)
                """,
                (clean_username, clean_email, pwd_hash, salt.hex(), clean_name),
            )
            user_id = cursor.lastrowid
        return {
            "id": user_id,
            "username": clean_username,
            "email": clean_email,
            "full_name": clean_name,
        }, None
    except sqlite3.IntegrityError as error:
        err_msg = str(error).lower()
        if "username" in err_msg:
            return None, "That username is already taken. Please choose another."
        if "email" in err_msg:
            return None, "An account with that email already exists."
        return None, "Could not create account. Please check your information."
    finally:
        conn.close()


def authenticate_user(username_or_email: str, password: str, db_path=None):
    init_db(db_path)
    clean_login = (username_or_email or "").strip()
    if not clean_login or not password:
        return None, "Please enter both your username/email and password."

    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, email, password_hash, salt, full_name
            FROM users
            WHERE username = ? OR email = ?
            """,
            (clean_login, clean_login.lower()),
        )
        row = cursor.fetchone()
        if not row:
            return None, "Invalid username or password."

        stored_hash = row["password_hash"]
        salt = bytes.fromhex(row["salt"])
        calculated_hash = _hash_password(password, salt)

        if calculated_hash != stored_hash:
            return None, "Invalid username or password."

        return {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"] or row["username"],
        }, None
    finally:
        conn.close()


def save_trip(user_id: int, destination_name: str, country: str, db_path=None) -> bool:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO saved_trips (user_id, destination_name, country)
                VALUES (?, ?, ?)
                """,
                (user_id, destination_name, country),
            )
        return True
    finally:
        conn.close()


def remove_saved_trip(user_id: int, destination_name: str, db_path=None) -> bool:
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                DELETE FROM saved_trips
                WHERE user_id = ? AND destination_name = ?
                """,
                (user_id, destination_name),
            )
        return True
    finally:
        conn.close()


def is_trip_saved(user_id: int, destination_name: str, db_path=None) -> bool:
    if not user_id:
        return False
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 1 FROM saved_trips
            WHERE user_id = ? AND destination_name = ?
            LIMIT 1
            """,
            (user_id, destination_name),
        )
        return cursor.fetchone() is not None
    finally:
        conn.close()


def get_saved_trips(user_id: int, db_path=None):
    if not user_id:
        return []
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, destination_name, country, saved_at
            FROM saved_trips
            WHERE user_id = ?
            ORDER BY saved_at DESC
            """,
            (user_id,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_saved_trips_count(user_id: int, db_path=None) -> int:
    if not user_id:
        return 0
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as cnt FROM saved_trips WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        return row["cnt"] if row else 0
    finally:
        conn.close()


def create_user_session(user_id: int, days_valid: int = 30, db_path=None) -> str:
    init_db(db_path)
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                """
                INSERT INTO user_sessions (session_token, user_id, expires_at)
                VALUES (?, ?, ?)
                """,
                (token, user_id, expires_at.isoformat()),
            )
        return token
    finally:
        conn.close()


def get_user_by_session(session_token: str, db_path=None):
    if not session_token:
        return None
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        cursor = conn.cursor()
        now_iso = datetime.now(timezone.utc).isoformat()
        cursor.execute(
            """
            SELECT u.id, u.username, u.email, u.full_name
            FROM user_sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.session_token = ? AND s.expires_at > ?
            LIMIT 1
            """,
            (session_token, now_iso),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"] or row["username"],
        }
    finally:
        conn.close()


def delete_user_session(session_token: str, db_path=None) -> bool:
    if not session_token:
        return False
    init_db(db_path)
    conn = get_db_connection(db_path)
    try:
        with conn:
            conn.execute(
                "DELETE FROM user_sessions WHERE session_token = ?",
                (session_token,),
            )
        return True
    finally:
        conn.close()

