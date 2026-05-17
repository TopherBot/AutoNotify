# Security Policy

## Supported Versions
| Version | Supported |
|---------|-----------|
| `master` (latest) | ✅ Yes |
| `v1.x` | ❌ No |

## Reporting a Vulnerability
If you discover a security vulnerability, please **do not** post it publicly.

1. Email us directly at **security@autonotify.io** (or reach out via **Telegram** @autonotify_security).
2. Include:
   - A concise description of the vulnerability
   - Steps to reproduce (including any payloads or scripts)
   - Potential impact and severity assessment
3. We will acknowledge receipt within 48 hours and aim to issue a fix or mitigation within 14 days.

## Responsible Disclosure
We appreciate responsible disclosure and will credit you in the release notes (unless you prefer anonymity).

---

## Security Practices
- All secrets are loaded from environment variables or files outside version control.
- Logs are written in append‑only mode and rotated securely.
- Dependency scanning is performed nightly via `pip-audit`.
- CI runs `bandit` and `ruff` linting for security‑related code smells.
