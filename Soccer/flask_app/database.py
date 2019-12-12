import sqlite3

from . import app

def fetchall(cursor):
  column_names = [column_description[0] for column_description in cursor.description]
  return [dict(zip(column_names, row)) for row in cursor]

db = sqlite3.connect('database.sqlite3', detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
db.execute('pragma foreign_keys=ON')
db.set_trace_callback(print)
