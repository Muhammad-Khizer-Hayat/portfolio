"""
Auto-reply bot for the contact form.

Flow:
  1. generate_reply_text()  -> tries Groq API for a personalized reply,
                                falls back to a static template on any failure.
  2. send_auto_reply()      -> sends that text to the visitor via Resend,
                                respecting a simple per-email rate limit.

Rate limiting is in-memory (a dict), so it resets on server restart.
That's fine for a portfolio site; swap for a DB/Redis if you ever need
it to persist across restarts or across multiple server processes.
"""

import time
import httpx
import resend

from .config import settings

# email -> last_sent_unix_timestamp
_last_sent: dict[str, float] = {}


STATIC_TEMPLATE = (
    "<p>Hi {name},</p>"
    "<p>Thanks for reaching out through my portfolio! I've received your message "
    "and will get back to you within 24-48 hours.</p>"
    "<p>Best,<br>{owner_name}</p>"
)


def _is_rate_limited(email: str) -> bool:
    last = _last_sent.get(email)
    if last is None:
        return False
    return (time.time() - last) < settings.AUTO_REPLY_RATE_LIMIT_SECONDS


def _mark_sent(email: str) -> None:
    _last_sent[email] = time.time()


def generate_reply_text(name: str, message: str) -> str:
    """Return HTML string for the auto-reply body. Tries Groq, falls back to static."""
    if not settings.GROQ_API_KEY:
        return STATIC_TEMPLATE.format(name=name, owner_name=settings.OWNER_NAME)

    prompt = (
        f"You are writing a short auto-reply email on behalf of {settings.OWNER_NAME}, "
        f"replying to a portfolio contact-form message from {name}.\n\n"
        f"Their message:\n\"\"\"\n{message}\n\"\"\"\n\n"
        "Write a brief (3-5 sentences), warm, professional reply that:\n"
        "- Thanks them by name\n"
        "- Acknowledges the specific topic of their message in one sentence\n"
        "- Says the real reply will come within 24-48 hours\n"
        "- Does NOT answer technical questions, make commitments, quote prices, "
        "or promise availability - just acknowledge and set expectations\n"
        "- Signs off as " + settings.OWNER_NAME + "\n\n"
        "Return ONLY the email body as simple HTML (use <p> tags), nothing else - "
        "no subject line, no preamble, no markdown fences."
    )

    try:
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GROQ_MODEL,
                "max_tokens": 300,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=15.0,
        )
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"].strip()
        if text:
            return text
    except Exception:
        # Any failure (timeout, bad key, rate limit, malformed response) -> fall back silently
        pass

    return STATIC_TEMPLATE.format(name=name, owner_name=settings.OWNER_NAME)


def send_auto_reply(name: str, to_email: str, message: str) -> bool:
    """
    Sends the auto-reply. Returns True if sent, False if skipped
    (rate-limited, disabled, or not configured). Never raises -
    an auto-reply failure should never break the main contact flow.
    """
    if not settings.AUTO_REPLY_ENABLED:
        return False
    if not settings.RESEND_API_KEY or not to_email:
        return False
    if _is_rate_limited(to_email):
        return False

    body_html = generate_reply_text(name, message)

    try:
        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            "from": settings.AUTO_REPLY_FROM,
            "to": to_email,
            "subject": f"Thanks for reaching out, {name}!",
            "html": body_html,
        })
        _mark_sent(to_email)
        return True
    except Exception:
        # Don't let an auto-reply failure surface as an error to the visitor
        return False