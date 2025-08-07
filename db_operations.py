import sqlite3
from datetime import datetime
import os

DB_PATH = 'consciousday.db'


def init_db():
    """Initialize database with proper structure"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create fresh table with timestamp column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                date TEXT NOT NULL,
                journal TEXT NOT NULL,
                intention TEXT NOT NULL,
                dream TEXT,
                priorities TEXT NOT NULL,
                reflection TEXT NOT NULL,
                strategy TEXT NOT NULL
            )
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON entries(date)')
        conn.commit()


def save_entry(journal, intention, dream, priorities, reflection, strategy):
    """Save a new journal entry"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO entries 
            (date, journal, intention, dream, priorities, reflection, strategy)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (current_date, journal, intention, dream, priorities, reflection, strategy))
        conn.commit()


def get_entry_by_date(date):
    """Get most recent entry for a date"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM entries 
            WHERE date = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (date,))
        return cursor.fetchone()


def get_all_dates():
    """Get all unique dates"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT date FROM entries 
            ORDER BY date DESC
        ''')
        return [row[0] for row in cursor.fetchall()]


def get_all_entries_by_date(date):
    """Get all entries for a specific date"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM entries 
            WHERE date = ?
            ORDER BY timestamp DESC
        ''', (date,))
        return cursor.fetchall()