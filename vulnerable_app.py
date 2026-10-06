from flask import Flask, request, render_template_string
import sqlite3
import subprocess

app = Flask(__name__)

DB = "users.db"

def get_db():
    return sqlite3.connect(DB)

@app.route("/")
def home():
    return render_template_string("""
    <h2>Welcome to Vulnerable App</h2>
    <ul>
      <li><a href="/login">Login Page</a></li>
      <li><a href="/ping?host=localhost">Ping Test</a></li>
      <li><a href="/profile?name=Guest">Profile Page</a></li>
    </ul>
    """)


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # VULNERABILITY 1: SQL injection through string concatenation
        query = "SELECT username FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        conn = get_db()
        row = conn.execute(query).fetchone()
        conn.close()

        if row:
            message = "Login successful"
        else:
            message = "Invalid credentials"

    return render_template_string("""
    <h2>Demo Login</h2>
    <form method="post">
      <input name="username" placeholder="Username">
      <input name="password" type="password" placeholder="Password">
      <button>Login</button>
    </form>
    <p>{{ message }}</p>
    """, message=message)

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")

    # VULNERABILITY 2: OS command injection
    result = subprocess.check_output("ping -n 1 " + host, shell=True, text=True)
    return "<pre>" + result + "</pre>"

@app.route("/profile")
def profile():
    name = request.args.get("name", "Guest")

    # VULNERABILITY 3: Reflected XSS
    return "<h2>Welcome " + name + "</h2>"

if __name__ == "__main__":
    app.run(debug=True)
