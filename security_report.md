# Secure Code Assessment — CodSoft Task 3

**Application reviewed:** Small Python Flask demonstration application  
**Reviewer:** Harshit Rawat  
**Assessment type:** Manual static source-code review  
**Date:** 2026

## 1. Objective

The CodSoft Task 3 brief requires selecting an application, examining source code for common security weaknesses and coding flaws, using static analysis or manual review, suggesting secure coding practices, and preparing a report with vulnerabilities and recommended fixes.

## 2. Scope

The review covers `vulnerable_app.py`, especially:
- `/login`
- `/ping`
- `/profile`
- Application configuration

No real user credentials or production systems are involved.

## 3. Findings summary

| ID | Finding | Severity | Location |
|---|---|---|---|
| SEC-01 | SQL injection risk | High | `/login` |
| SEC-02 | OS command injection risk | High | `/ping` |
| SEC-03 | Reflected XSS risk | Medium | `/profile` |
| SEC-04 | Debug mode enabled | Medium | Application startup |

## 4. Detailed findings

### SEC-01 — SQL injection risk
**Severity:** High

The vulnerable version builds the SQL statement by concatenating user-controlled `username` and `password` values into the query.

**Risk:** Untrusted input can alter the intended SQL statement and may allow unauthorized database access.

**Recommendation:** Use parameterized queries / prepared statements. Validate input length and format, and never construct SQL by concatenating request data.

**Implemented fix:** `secure_app.py` uses SQLite placeholders and passes values separately.

### SEC-02 — OS command injection risk
**Severity:** High

The `/ping` endpoint places the `host` request parameter directly into a shell command and enables `shell=True`.

**Risk:** User-controlled input reaching a shell can cause unintended operating-system commands to execute.

**Recommendation:** Avoid shell invocation for user input. Validate the input against an allow-list or strict format and pass arguments as a list to `subprocess.run`.

**Implemented fix:** The secure version accepts an IP address, validates it with `ipaddress`, uses an argument list, disables shell execution, and applies a timeout.

### SEC-03 — Reflected XSS risk
**Severity:** Medium

The vulnerable `/profile` endpoint concatenates the `name` request parameter directly into an HTML response.

**Risk:** HTML/JavaScript supplied by an attacker could be reflected into a victim's browser.

**Recommendation:** Use a templating engine with automatic escaping and avoid inserting raw request data into HTML.

**Implemented fix:** The secure version passes `name` as a Jinja template variable.

### SEC-04 — Debug mode enabled
**Severity:** Medium

The vulnerable application starts Flask with `debug=True`.

**Risk:** Debug features can expose implementation details and should not be enabled in production.

**Recommendation:** Disable debug mode in production and use controlled logging and error handling.

**Implemented fix:** The secure version explicitly sets `DEBUG = False`.

## 5. Secure coding practices

1. Treat all external input as untrusted.
2. Use parameterized database queries.
3. Avoid `shell=True` with request-derived data.
4. Validate input with strict allow-lists where practical.
5. Use framework-provided output encoding/escaping.
6. Disable debug mode in production.
7. Apply authentication and authorization checks to protected resources.
8. Store passwords using a strong password-hashing algorithm rather than plaintext.
9. Keep dependencies updated and review security advisories.
10. Run static analysis and dependency checks as part of development.

## 6. Static-analysis plan

The project can be checked with Bandit:

```bash
python -m pip install bandit
bandit -r vulnerable_app.py
```

The assessment also includes a manual review because automated tools may not identify every application-specific security problem.

## 7. Verification checklist

- [x] SQL query changed to parameterized form
- [x] Shell execution removed
- [x] Input validation added to ping endpoint
- [x] Output escaping added
- [x] Debug mode disabled
- [x] Security recommendations documented

## 8. Conclusion

The reviewed demonstration application contained several common security weaknesses involving untrusted input, command execution, output handling, and development configuration. The secure version demonstrates practical remediation patterns. The application is intentionally small so that each weakness and its fix can be clearly understood during the CodSoft presentation.

**Educational note:** This project is designed for authorized code-review and secure-coding education. It does not target any third-party system.
