from flask import Flask, request, render_template_string
import sqlite3
import subprocess
import ipaddress

app = Flask(__name__)
app.config["DEBUG"] = False

DB = "users.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template_string("""
    <h2>Welcome to Secure App</h2>
    <ul>
      <li><a href="/login">Login Page</a></li>
      <li><a href="/ping?host=127.0.0.1">Ping Test</a></li>
      <li><a href="/profile?name=Guest">Profile Page</a></li>
    </ul>
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # FIX: parameterized SQL query
        query = "SELECT username FROM users WHERE username = ? AND password = ?"
        conn = get_db()
        row = conn.execute(query, (username, password)).fetchone()
        conn.close()

        message = "Login successful" if row else "Invalid credentials"

    return render_template_string("""
    <h2>Demo Login</h2>
    <form method="post">
      <input name="username" maxlength="50">
      <input name="password" type="password" maxlength="100">
      <button>Login</button>
    </form>
    <p>{{ message }}</p>
    """, message=message)

@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # FIX: validate input and avoid shell=True
    try:
        ipaddress.ip_address(host)
    except ValueError:
        return "Invalid host", 400

    result = subprocess.run(
        ["ping", "-n", "1", host],
        capture_output=True,
        text=True,
        timeout=5,
        check=False
    )
    return "<pre>" + result.stdout + "</pre>"

@app.route("/profile")
def profile():
    name = request.args.get("name", "Guest")

    # FIX: Jinja2 escapes HTML by default
    return render_template_string("<h2>Welcome {{ name }}</h2>", name=name)

if __name__ == "__main__":
    app.run(debug=False)
