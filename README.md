# CodSoft Task 3 — Secure Code Assessment

A small Python Flask application used to demonstrate a security-focused source-code review.

## Included

- `vulnerable_app.py` — intentionally insecure training sample
- `secure_app.py` — remediation version
- `security_report.md` — assessment report
- `requirements.txt` — dependency list

## Vulnerabilities reviewed

- SQL injection risk
- OS command injection risk
- Reflected XSS risk
- Flask debug mode enabled

## Run

```bash
python -m venv venv
```

Git Bash:
```bash
source venv/Scripts/activate
```

Install:
```bash
python -m pip install -r requirements.txt
```

Run either version:
```bash
python vulnerable_app.py
```

or:
```bash
python secure_app.py
```

Use the vulnerable version only in a local, isolated training environment.

## Static analysis

Optional Bandit scan:

```bash
python -m pip install bandit
bandit -r vulnerable_app.py
```

## Author

Harshit Rawat
