from flask import Flask, g, request, render_template
import sys
import sqlite3

app = Flask(__name__)

# db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('db.sq3')
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


# save snippet into database
def save_snippet(v, ip):
  get_db().cursor().execute("INSERT INTO t (v, ip) VALUES (?, ?)", (v, ip))
  get_db().commit()


# get snippets
def get_snippets(lim):
  return [row for row in get_db().cursor().execute("SELECT * FROM t ORDER BY ts DESC LIMIT %s" % lim)]

# the only route
@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
      # save to database
      data = request.get_data()
      save_snippet(data, request.remote_addr)
      return "OK\n"
    else:
      # show the contents
      return render_template('list.html', recs=get_snippets(100))

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=int(sys.argv[1]) if len(sys.argv) - 1 else 80)