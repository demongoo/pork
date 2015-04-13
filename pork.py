from flask import Flask, g
import sys
import sqlite3

app = Flask(__name__)

# in memory db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(":memory:")
        db.cursor().execute('''
            CREATE TABLE IF NOT EXISTS t (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              v TEXT,
              ip TEXT,
              ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        ''')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# the only route
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(port=sys.argv[1] if len(sys.argv) - 1 else 80)