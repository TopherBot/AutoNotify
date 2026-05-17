# AutoNotify

**AutoNotify** is a lightweight, extensible monitoring & notification system written in Python. It watches arbitrary health‑check endpoints (HTTP, TCP, custom scripts), records structured logs, and pushes alerts to Telegram, Email, or Slack.

---

## Features
- ✅ Pluggable health‑check backends (HTTP, TCP, command line)
- ✅ Structured JSON logging with rotating file handler
- ✅ Asynchronous monitoring using `asyncio`
- ✅ Automatic notification routing (Telegram Bot API, SMTP, Slack webhook)
- ✅ Runtime configuration reload (via `SIGHUP`)
- ✅ Docker‑ready, CI/CD friendly
- ✅ Full security policy (see `SECURITY.md`)

---

## Quick Start
```bash
# Clone the repo
git clone https://github.com/youruser/autonotify.git
cd autonotify

# Create a virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy the example config and edit your secrets
cp config/example.yaml config/config.yaml
# edit config/config.yaml → set telegram token, chat_id, email creds, etc.

# Run the service
python -m autonotify
```

---

## Configuration
All settings live in `config/config.yaml`. Example snippet:
```yaml
# config/config.yaml
monitor:
  interval_seconds: 30
  checks:
    - name: "Google"
      type: http
      url: "https://www.google.com"
      expected_status: 200
    - name: "Redis"
      type: tcp
      host: "localhost"
      port: 6379

notifications:
  telegram:
    enabled: true
    token: "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
  email:
    enabled: false
    smtp_server: "smtp.example.com"
    smtp_port: 587
    username: "alert@example.com"
    password: "supersecret"
    from_addr: "alert@example.com"
    to_addrs:
      - "admin@example.com"
```

---

## Logging
Logs are written to `logs/autonotify.log` in JSON format with rotation (5 MB per file, keep 7). Use tools like `jq` or `logstash` to ingest.

---

## Contributing
1. Fork the repo
2. Create a feature branch (`git checkout -b feat/awesome`)
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Run tests: `pytest -q`
5. Submit a Pull Request

---

## License
MIT – see `LICENSE` file.
