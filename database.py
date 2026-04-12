"""SQLite helpers for storing game results."""
import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


DB_PATH = Path(__file__).resolve().parent / "game_results.db"
LOCAL_TIMEZONE = ZoneInfo("Asia/Ho_Chi_Minh")


class GameDatabase:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS game_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    level INTEGER NOT NULL,
                    played_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS app_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
                """
            )

    def _current_local_timestamp(self):
        return datetime.now(LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S")

    def save_result(self, player_name, score, level):
        clean_name = player_name.strip() or "Anonymous"
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO game_results (player_name, score, level, played_at)
                VALUES (?, ?, ?, ?)
                """,
                (clean_name, int(score), int(level), self._current_local_timestamp()),
            )

    def get_top_results(self, limit=5):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT player_name, score, level, played_at
                FROM game_results
                ORDER BY score DESC, played_at ASC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return rows
