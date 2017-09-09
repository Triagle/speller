import sys, os
import pytest
import sqlite3

DATABASE_LOCATION = 'db/data.db'

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)


@pytest.fixture(scope="session")
def db_conn():

    with sqlite3.connect('db/data.db') as conn:
        yield conn
        conn.rollback()
